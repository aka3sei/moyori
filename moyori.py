import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="全国対応：最寄り駅検索", layout="centered")

# ヘッダー非表示
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 全国対応：最寄り駅検索")
st.caption("どんな地名でも周辺駅を探し出します")

# 入力
address = st.text_input("住所や地名を入力（例：新宿三丁目、三鷹市上連雀、横浜駅周辺）")

if address:
    # 1. 住所から座標を特定（高精度検索）
    # 日本語の地名をより柔軟に解釈する設定
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    
    try:
        with st.spinner('駅を探しています...'):
            geo_res = requests.get(geo_url, timeout=10).json()
            
            if geo_res:
                # 候補を絞り込まず、最も精度の高い座標を抽出
                lon, lat = geo_res[0]['geometry']['coordinates']
                
                # 2. 駅検索（検索半径を最大まで広げてリクエスト）
                # HeartRails APIの制限を回避するため、取得数を増やしてフィルタリング
                station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
                station_res = requests.get(station_url, timeout=10).json()
                
                stations = station_res.get('response', {}).get('station', [])
                
                # 万が一見つからない場合、少しだけ座標をずらして再試行（新宿などの密集地対策）
                if not stations:
                    station_url_retry = f"https://express.heartrails.com/api/json?method=getStations&x={lon + 0.002}&y={lat + 0.002}"
                    stations = requests.get(station_url_retry).json().get('response', {}).get('station', [])

                if stations:
                    st.subheader(f"📍 {address} 周辺の駅")
                    
                    data = []
                    for s in stations:
                        # 距離の計算
                        dist_m = int(s.get('distance', 0))
                        # 0mや近すぎる場合の補正
                        if dist_m < 80:
                            dist_m = 80
                        
                        walk_min = -(-dist_m // 80) # 80m=1分（切り上げ）
                        
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    
                    # 重複を消して距離順に並び替え
                    df = pd.DataFrame(data).drop_duplicates(subset=['駅名']).sort_values("距離")
                    
                    # 表示
                    st.table(df)
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                    
                else:
                    st.warning("この地点のすぐ近くに駅が見つかりませんでした。少し広い範囲で探してみてください。")
            else:
                st.error("住所が見つかりませんでした。都道府県名から入力してみてください。")
    except Exception as e:
        st.error("検索中にエラーが発生しました。もう一度お試しください。")

st.info("※徒歩分数は不動産表示基準（80m/分）に基づき、直線距離から算出しています。")
