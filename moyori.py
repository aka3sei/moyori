import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="最寄り駅検索ツール", layout="centered")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索")
st.caption("住所から周辺の駅と徒歩分数を表示します")

address = st.text_input("住所を入力してください", placeholder="例：三鷹市上連雀1丁目")

if address:
    # 1. 住所を緯度経度に変換
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    
    try:
        geo_res = requests.get(geo_url, timeout=10).json()
        
        lat, lon = None, None
        if geo_res:
            # 【重要】複数の候補から座標(geometry)を持っているものを探す
            for candidate in geo_res:
                if 'geometry' in candidate and 'coordinates' in candidate['geometry']:
                    lon, lat = candidate['geometry']['coordinates']
                    break # 座標が見つかったらループを抜ける
        
        if lat and lon:
            # 2. 最寄り駅を取得
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url, timeout=10).json()
            
            stations = station_res.get('response', {}).get('station', [])
            
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                data = []
                for s in stations:
                    try:
                        dist_val = s.get('distance')
                        if dist_val is None: continue
                        
                        dist_m = int(dist_val)
                        walk_min = -(-dist_m // 80)
                        
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    except: continue
                
                if data:
                    st.table(pd.DataFrame(data))
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                else:
                    st.warning("周辺に駅が見つかりませんでした。")
            else:
                st.warning("駅情報の取得に失敗しました。時間をおいて試してください。")
        else:
            st.error("入力された住所の場所を特定できませんでした。もう少し詳しい住所を入力してください。")
            
    except Exception as e:
        st.error(f"システムエラー: {e}")
