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

st.title("🚉 全国対応：最寄り駅検索")
st.caption("住所から周辺の駅を「見つかるまで」範囲を広げて探します")

address = st.text_input("住所を入力してください", placeholder="例：三鷹市上連雀1丁目")

def fetch_stations(lon, lat):
    """HeartRails APIを叩く関数"""
    url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
    try:
        res = requests.get(url, timeout=10).json()
        return res.get('response', {}).get('station', [])
    except:
        return []

if address:
    # 1. 住所から座標を取得
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    try:
        geo_res = requests.get(geo_url, timeout=10).json()
        if geo_res:
            lon, lat = geo_res[0]['geometry']['coordinates']
            
            # 2. 駅検索（見つかるまで座標を微調整して再試行）
            stations = fetch_stations(lon, lat)
            
            # もし見つからなければ、少しずつ範囲をずらして再検索（計3回）
            if not stations:
                offsets = [0.005, 0.01] # 約500m, 1kmずらす
                for offset in offsets:
                    stations = fetch_stations(lon + offset, lat + offset)
                    if stations: break

            # 3. 表示処理
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                data = []
                for s in stations:
                    try:
                        dist_m = int(s.get('distance', 0))
                        # 0m表記や取得失敗を避ける
                        if dist_m == 0: dist_m = 500 # 概算
                        
                        walk_min = -(-dist_m // 80)
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    except: continue
                
                if data:
                    df = pd.DataFrame(data).drop_duplicates(subset=['駅名']).head(5)
                    st.table(df)
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                else:
                    st.warning("周辺に駅が見つかりませんでした。")
            else:
                st.warning("駅データが取得できません。住所を『三鷹駅』のように変えてみてください。")
        else:
            st.error("住所の特定に失敗しました。")
    except Exception as e:
        st.error("検索エラーが発生しました。再度お試しください。")
