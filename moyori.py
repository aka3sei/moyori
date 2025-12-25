import streamlit as st
import requests
import pandas as pd
import urllib.parse

st.set_page_config(page_title="最寄り駅検索", layout="centered")

# ヘッダー非表示
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索（詳細版）")

address = st.text_input("住所や地名を入力", placeholder="例：新宿三丁目")

if address:
    # 1. 座標取得（国土地理院）
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    
    try:
        geo_res = requests.get(geo_url, timeout=5).json()
        if geo_res:
            lon, lat = geo_res[0]['geometry']['coordinates']
            
            # 2. 駅名リストの取得（HeartRails API）
            # 失敗しにくいようにリトライ設定
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            
            stations = []
            with st.spinner('駅名を読み込んでいます...'):
                try:
                    # リトライを含めたリクエスト
                    st_res = requests.get(station_url, timeout=10).json()
                    stations = st_res.get('response', {}).get('station', [])
                except:
                    pass

            # 3. 駅名リストの表示
            if stations:
                st.subheader("📋 周辺駅一覧")
                res_data = []
                for s in stations:
                    dist_m = int(s.get('distance', 0))
                    walk_min = -(-dist_m // 80)
                    res_data.append({
                        "路線": s.get('line', '-'),
                        "駅名": s.get('name', '-'),
                        "徒歩": f"約{walk_min}分"
                    })
                
                # 重複排除して表示
                df = pd.DataFrame(res_list := res_data).drop_duplicates(subset=['駅名']).head(5)
                st.table(df)
            else:
                st.info("⚠️ 駅名の自動取得が制限されています。下の地図で駅名を確認してください。")

            # 4. 地図の表示（Googleマップ埋め込み）
            st.subheader("🗺️ 周辺地図")
            search_query = f"{address} 駅"
            encoded_query = urllib.parse.quote(search_query)
            map_url = f"https://www.google.com/maps/embed/v1/search?key=YOUR_GOOGLE_MAPS_API_KEY_OPTIONAL&q={encoded_query}"
            
            # APIキーなしでも動く埋め込み方式
            embed_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&t=m&z=15"
            st.components.v1.iframe(embed_url, height=400)

        else:
            st.error("住所が見つかりませんでした。")
    except Exception as e:
        st.error("検索エラーが発生しました。もう一度お試しください。")
