import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="最寄り駅検索ツール", layout="centered")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索")
st.caption("高精度エンジンで周辺駅を特定します")

address = st.text_input("住所を入力してください", placeholder="例：三鷹市上連雀1丁目")

if address:
    # 1. 住所を緯度経度に変換 (OSM Nominatim API を使用して精度を向上)
    # ユーザーエージェントを設定しないとエラーになるため設定
    headers = {'User-Agent': 'MyRealEstateApp/1.0'}
    geo_url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
    
    try:
        geo_res = requests.get(geo_url, headers=headers, timeout=10).json()
        
        if geo_res:
            lat = float(geo_res[0]['lat'])
            lon = float(geo_res[0]['lon'])
            
            # 2. 最寄り駅を取得 (HeartRails Express API)
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url, timeout=10).json()
            
            stations = station_res.get('response', {}).get('station', [])
            
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                data = []
                for s in stations:
                    try:
                        dist_m = int(s.get('distance', 0))
                        walk_min = -(-dist_m // 80) # 80m=1分
                        
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    except: continue
                
                if data:
                    df = pd.DataFrame(data)
                    st.table(df)
                    # 地図表示
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                else:
                    st.warning("周辺に駅が見つかりませんでした。")
            else:
                st.warning("駅データが取得できませんでした。住所を『三鷹市下連雀』などに変えてお試しください。")
        else:
            st.error("入力された住所の場所を特定できませんでした。都道府県名から入力してみてください。")
            
    except Exception as e:
        st.error("現在、検索サーバーが混み合っています。少し待ってから再度「Enter」を押してください。")
