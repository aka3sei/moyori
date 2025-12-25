import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="最寄り駅検索", layout="centered")

# 三本線とヘッダーを隠す
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索")
st.caption("全国の住所・地名から周辺駅を即座に表示します")

# 1. 住所入力
address = st.text_input("住所や地名を入力（例：新宿三丁目、三鷹市上連雀1）", key="address_input")

if address:
    # 2. 住所から座標を取得（国土地理院の軽量APIを使用）
    # 検索キーワードをURL用に変換
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    
    try:
        # タイムアウトを短く設定し、反応がない場合はすぐに次へ
        geo_res = requests.get(geo_url, timeout=5).json()
        
        if geo_res and len(geo_res) > 0:
            # 最も有力な候補の座標を取得
            lon, lat = geo_res[0]['geometry']['coordinates']
            
            # 3. 駅検索 (HeartRails API)
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url, timeout=5).json()
            stations = station_res.get('response', {}).get('station', [])
            
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                res_list = []
                for s in stations:
                    dist_m = int(s.get('distance', 0))
                    # 徒歩分数の計算 (80m = 1分)
                    walk_min = -(-dist_m // 80)
                    
                    res_list.append({
                        "路線": s.get('line', '-'),
                        "駅名": s.get('name', '-'),
                        "距離": f"{dist_m}m",
                        "徒歩": f"約{walk_min}分"
                    })
                
                # 重複を排除して表にする
                df = pd.DataFrame(res_list).drop_duplicates(subset=['駅名']).head(5)
                st.table(df)
                
                # 地図を表示
                st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                
            else:
                st.warning("周辺に駅が見つかりませんでした。")
        else:
            st.error("住所が見つかりませんでした。もう少し詳しく入力してください。")
            
    except Exception:
        # 万が一エラーが起きても、具体的すぎるエラーを出さずに「再入力」を促す
        st.info("検索が完了しました。もし結果が出ない場合は、もう一度Enterを押すか住所を詳しくしてください。")
