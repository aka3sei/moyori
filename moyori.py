import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="最寄り駅検索ツール", layout="centered")

# 三本線とヘッダーを消す設定
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索")
st.caption("住所から周辺の駅と徒歩分数を一括表示します")

# 1. 住所入力
address = st.text_input("住所を入力してください", placeholder="例：東京都武蔵野市中町1-1-1")

if address:
    # 緯度経度に変換（国土地理院やOSMの無料APIを利用する簡易版）
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    geo_res = requests.get(geo_url).json()

    if geo_res:
        lon, lat = geo_res[0]['geometry']['coordinates']
        
        # 2. 最寄り駅を取得 (HeartRails Express API)
        station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
        station_res = requests.get(station_url).json()
        
        stations = station_res.get('response', {}).get('station', [])
        
        if stations:
            st.subheader(f"📍 {address} の最寄り駅")
            
            data = []
            for s in stations:
                # 距離から徒歩分数を計算 (80m = 1分, 切り上げ)
                dist_m = int(s['distance'])
                walk_min = -(-dist_m // 80) # 切り上げ計算
                
                data.append({
                    "路線": s['line'],
                    "駅名": s['name'],
                    "距離": f"{dist_m}m",
                    "徒歩": f"{walk_min}分"
                })
            
            # 結果をテーブル表示
            df = pd.DataFrame(data)
            st.table(df)
            
            # 地図表示
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        else:
            st.warning("付近に駅が見つかりませんでした。")
    else:
        st.error("住所の特定に失敗しました。番地まで正しく入力してください。")