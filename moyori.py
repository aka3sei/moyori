import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="最寄り駅検索ツール", layout="centered")

# デザイン調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    .stTable { font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索")
st.caption("住所から周辺の駅と徒歩分数を表示します")

# 住所入力（プレースホルダを具体的に）
address = st.text_input("住所を入力してください", placeholder="例：三鷹市上連雀1")

if address:
    # 1. 住所を緯度経度に変換（住所検索API）
    # 検索キーワードをURLエンコードして安全に送信
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    
    try:
        geo_res = requests.get(geo_url, timeout=5).json()
        
        if geo_res and len(geo_res) > 0:
            # 最初の候補の座標を取得
            lon, lat = geo_res[0]['geometry']['coordinates']
            
            # 2. 最寄り駅を取得 (HeartRails Express API)
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url, timeout=5).json()
            
            # APIのレスポンス構造を安全に解析
            response_data = station_res.get('response', {})
            stations = response_data.get('station', [])
            
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                data = []
                for s in stations:
                    try:
                        # 距離の取得と変換
                        dist_val = s.get('distance')
                        if dist_val is None: continue
                        
                        dist_m = int(dist_val)
                        # 徒歩分数の計算 (80m = 1分, 切り上げ)
                        walk_min = -(-dist_m // 80)
                        
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    except (ValueError, TypeError):
                        continue
                
                if data:
                    # 表形式で表示
                    df = pd.DataFrame(data)
                    st.table(df)
                    
                    # 地図で場所を確認
                    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                    st.map(map_data)
                else:
                    st.warning("周辺に駅の情報が見つかりませんでした。")
            else:
                # 駅が見つからない場合、少し検索範囲を広げるヒントを出す
                st.warning("付近に駅が見つかりませんでした。住所をもう少し詳しく入力してみてください。")
        else:
            st.error("入力された住所から場所を特定できませんでした。")
            
    except requests.exceptions.Timeout:
        st.error("検索サーバーが混み合っています。もう一度「Enter」を押してください。")
    except Exception as e:
        st.error(f"エラーが発生しました。")
