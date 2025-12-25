import streamlit as st
import requests
import pandas as pd

# ページ設定
st.set_page_config(page_title="最寄り駅検索ツール", layout="centered")

# ヘッダー非表示・余白調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索")
st.caption("全国の住所から周辺駅と徒歩分数を即座に算出します")

# 1. 住所入力
address = st.text_input("住所や地名を入力（例：新宿三丁目、三鷹市上連雀）", key="addr_input")

if address:
    try:
        # 2. 座標取得（国土地理院API：比較的安定しており、制限も緩い）
        geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
        geo_res = requests.get(geo_url, timeout=5)
        geo_data = geo_res.json()

        if geo_data:
            # 座標を抽出
            lon, lat = geo_data[0]['geometry']['coordinates']
            
            # 3. 駅検索（HeartRails API）
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url, timeout=5)
            station_data = station_res.json()
            
            stations = station_data.get('response', {}).get('station', [])
            
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                # 表示用リスト作成
                results = []
                for s in stations:
                    dist_m = int(s.get('distance', 0))
                    # 徒歩分数の計算（不動産基準：80m＝1分）
                    walk_min = -(-dist_m // 80)
                    
                    results.append({
                        "路線": s.get('line', '-'),
                        "駅名": s.get('name', '-'),
                        "距離": f"{dist_m}m",
                        "徒歩": f"約{walk_min}分"
                    })
                
                # 重複を排除し、距離順に上位を表示
                df = pd.DataFrame(results).drop_duplicates(subset=['駅名']).head(5)
                st.table(df)
                
                # 位置確認マップ
                st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
            else:
                st.warning("周辺に駅が見つかりませんでした。番地まで入力してみてください。")
        else:
            st.error("住所の場所を特定できませんでした。")

    except Exception:
        # エラーが発生しても、赤い警告ではなく、実務を妨げない優しい案内を表示
        st.info("💡 検索エンジンの応答待ちです。再度「Enter」を押すか、住所を少し詳しく入力してみてください。")

st.divider()
st.caption("※本データは直線距離に基づく概算です。正確な経路は地図アプリ等でご確認ください。")
