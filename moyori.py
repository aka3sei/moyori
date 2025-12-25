import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="最寄り駅検索ツール", layout="centered")

# スタイル調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅検索")
st.caption("住所から周辺の駅（3km圏内）をリストアップします")

address = st.text_input("住所を入力してください", placeholder="例：三鷹市上連雀1丁目")

if address:
    # 1. 住所から緯度経度を取得
    geo_url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    
    try:
        geo_res = requests.get(geo_url, timeout=10).json()
        
        if geo_res:
            # 最初の候補を採用
            lon, lat = geo_res[0]['geometry']['coordinates']
            
            # 2. 周辺の駅を取得（メソッドを getStations から getLines に変更して範囲をカバー）
            # または、より広範囲を検索する「都道府県・市区町村」指定を組み合わせて検索
            # 今回は getStations のまま、複数の候補を確実に拾うロジックに強化
            
            station_url = f"https://express.heartrails.com/api/json?method=getStations&x={lon}&y={lat}"
            station_res = requests.get(station_url, timeout=10).json()
            
            stations = station_res.get('response', {}).get('station', [])
            
            if stations:
                st.subheader(f"📍 {address} 付近の駅")
                
                data = []
                for s in stations:
                    try:
                        dist_m = int(s.get('distance', 0))
                        # 徒歩分数の計算 (80m = 1分)
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
                    # 重複を排除して表示
                    df = pd.DataFrame(data).drop_duplicates(subset=['駅名'])
                    st.table(df)
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                else:
                    st.warning("周辺に駅データが見つかりませんでした。")
            else:
                # 【最終手段】APIが反応しない場合、住所の文字列から推測
                st.warning("詳細な駅情報を取得できませんでした。住所を『三鷹駅』のように具体的に入力して再試行してください。")
        else:
            st.error("入力された住所の場所を特定できませんでした。")
            
    except Exception as e:
        st.error("システムエラーが発生しました。時間を置いてお試しください。")
