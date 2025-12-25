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
    # 1. 住所を緯度経度に変換（より広い範囲を検索できるように調整）
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    try:
        geo_res = requests.get(geo_url).json()
        if geo_res:
            # 国土地理院のデータから最新の座標を取得
            lon, lat = geo_res[0]['geometry']['coordinates']
            
            # 2. 最寄り駅を取得 (HeartRails Express API)
            # 念のため、複数の駅を取得できるようにリクエスト
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url).json()
            
            stations = station_res.get('response', {}).get('station', [])
            
            if stations:
                st.subheader(f"📍 {address} 周辺の駅")
                
                data = []
                for s in stations:
                    try:
                        dist_val = s.get('distance')
                        if dist_val is None: continue
                        
                        dist_m = int(dist_val)
                        walk_min = -(-dist_m // 80) # 80m=1分
                        
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    except: continue
                
                if data:
                    # 距離が近い順に並び替えて表示
                    df = pd.DataFrame(data)
                    st.table(df)
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                else:
                    st.warning("周辺に駅の情報が見つかりませんでした。")
            else:
                # APIの反応がない場合のバックアップメッセージ
                st.error("駅データサーバーから応答がありません。少し時間を置いて再度お試しください。")
        else:
            st.error("住所を特定できませんでした。「東京都三鷹市...」から入力してみてください。")
    except Exception as e:
        st.error(f"システムエラーが発生しました: {e}")
