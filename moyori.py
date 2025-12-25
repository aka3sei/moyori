import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="最寄り駅検索ツール", layout="centered")

# スタイル設定
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 全国対応：最寄り駅検索")
st.caption("住所から周辺の駅と徒歩分数を一括表示します")

address = st.text_input("住所を入力してください", placeholder="例：横浜市中区山下町")

if address:
    # 1. 住所から座標を取得
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    try:
        geo_res = requests.get(geo_url, timeout=10).json()
        if geo_res:
            lon, lat = geo_res[0]['geometry']['coordinates']
            
            # 2. 駅検索（メイン：駅データ.jp系API）
            # 緯度経度から周辺の駅を取得するURL
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url, timeout=10).json()
            stations = station_res.get('response', {}).get('station', [])
            
            # 3. 表示処理
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                data = []
                for s in stations:
                    try:
                        # 距離の取得
                        dist_m = int(s.get('distance', 0))
                        if dist_m == 0: continue
                        
                        # 不動産基準の計算 (80m = 1分)
                        walk_min = -(-dist_m // 80)
                        
                        data.append({
                            "路線": s.get('line', '-'),
                            "駅名": s.get('name', '-'),
                            "距離": f"{dist_m}m",
                            "徒歩": f"約{walk_min}分"
                        })
                    except:
                        continue
                
                if data:
                    # 距離が近い順に最大5件表示
                    df = pd.DataFrame(data).sort_values("距離").head(5)
                    st.table(df)
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                else:
                    st.warning("周辺に駅データが見つかりませんでした。")
            else:
                # 4. バックアップ：住所が「1丁目」などで止まっている場合に、少し範囲を広げるヒント
                st.info("詳細な駅データが見つかりませんでした。住所に番地を追加するか、建物名を入れてみてください。")
        else:
            st.error("住所の特定に失敗しました。都道府県から入力してください。")
    except Exception as e:
        st.error("現在、検索サーバーが反応していません。再度お試しください。")
