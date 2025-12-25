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

def get_stations(lon, lat):
    """HeartRails APIから駅を取得する関数"""
    url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
    try:
        res = requests.get(url, timeout=10).json()
        return res.get('response', {}).get('station', [])
    except:
        return []

if address:
    # 1. 住所を緯度経度に変換
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    
    try:
        geo_res = requests.get(geo_url, timeout=10).json()
        
        target_lon, target_lat = None, None
        if geo_res:
            for candidate in geo_res:
                if 'geometry' in candidate and 'coordinates' in candidate['geometry']:
                    target_lon, target_lat = candidate['geometry']['coordinates']
                    break
        
        if target_lat and target_lon:
            # 2. 最寄り駅を取得（1回目）
            stations = get_stations(target_lon, target_lat)
            
            # 【重要】もし見つからなかったら、座標を少しずらして再試行（APIの隙間対策）
            if not stations:
                stations = get_stations(target_lon + 0.001, target_lat + 0.001)

            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                data = []
                for s in stations:
                    try:
                        dist_m = int(s.get('distance', 0))
                        if dist_m == 0: continue
                        
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
                    st.map(pd.DataFrame({'lat': [target_lat], 'lon': [target_lon]}))
                else:
                    st.warning("周辺に有効な駅データが見つかりませんでした。")
            else:
                st.warning("駅情報が取得できませんでした。住所を「三鷹駅」のように変えて試してみてください。")
        else:
            st.error("入力された住所の場所を特定できませんでした。")
            
    except Exception as e:
        st.error(f"システムエラーが発生しました。")
