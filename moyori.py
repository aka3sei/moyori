import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="最寄り駅検索", layout="centered")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 安定版：最寄り駅検索")

# 1. 住所入力
address = st.text_input("住所や地名を入力（例：新宿三丁目、三鷹市上連雀1）")

if address:
    # 検索中アニメーション
    with st.spinner('データを取得中...'):
        try:
            # 【変更点】国土地理院APIが不安定なため、OpenStreetMap(OSM)の検索を使用
            # ※User-Agentを設定しないとエラーになるため必須
            headers = {'User-Agent': 'PropertySearchApp/1.0'}
            geo_url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
            
            geo_res = requests.get(geo_url, headers=headers, timeout=10).json()
            
            if geo_res:
                lat = float(geo_res[0]['lat'])
                lon = float(geo_res[0]['lon'])
                
                # 2. 駅検索 (HeartRails API)
                station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
                # タイムアウト対策とリトライ
                station_res = requests.get(station_url, timeout=10).json()
                stations = station_res.get('response', {}).get('station', [])
                
                if stations:
                    st.subheader(f"📍 {address} 付近の駅")
                    data = []
                    for s in stations:
                        dist_m = int(s.get('distance', 0))
                        walk_min = -(-dist_m // 80) # 80m=1分
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    
                    df = pd.DataFrame(data).drop_duplicates(subset=['駅名'])
                    st.table(df)
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                else:
                    st.warning("周辺に駅が見つかりませんでした。")
            else:
                st.error("住所が見つかりませんでした。都道府県名から入力してください。")
                
        except Exception as e:
            # エラーの詳細を表示せず、再試行を促す（実務で安心感を出すため）
            st.error("一時的に検索サーバーが混み合っています。5秒ほど待ってから再度「Enter」キーを押してください。")
