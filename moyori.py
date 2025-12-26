import streamlit as st
import urllib.parse
from streamlit_js_eval import get_geolocation

# 1. ページ設定
st.set_page_config(page_title="最寄り駅・周辺検索", layout="centered")

# ヘッダー非表示・余白調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    /* 地図の角を丸くする */
    iframe { border-radius: 15px; border: 1px solid #ddd; }
    /* ボタンのスタイル調整 */
    div.stButton > button {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")

# 2. 住所入力
address = st.text_input("住所や地名を入力してください", placeholder="例：新宿三丁目、三鷹市上連雀1")

st.info("住所を入力してEnterを押すと、周辺の駅が地図上に一覧表示されます。")

# --- 現在地検索ボタンの追加 ---
st.write("または、スマートフォンのGPSを使用して検索します。")
loc = None
if st.button("📍 現在地で最寄り駅を検索", use_container_width=True):
    # ブラウザから位置情報を取得（許可を求めるポップアップが出ます）
    loc = get_geolocation()

# 検索対象の決定
search_target = None
if address:
    search_target = address
elif loc:
    # 緯度・経度が得られた場合
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    search_target = f"{lat},{lon}"

# 3. 表示処理
if search_target:
    # 検索クエリの作成
    search_query = f"{search_target} 最寄り駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURLの設定
    map_url = f"https://www.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja"
    
    label = "現在地" if search_target == f"{lat},{lon}" if 'lat' in locals() else address else address
    st.subheader(f"📍 {label} 付近の駅情報")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    st.success("上の地図内で、最寄り駅と徒歩ルートを確認できます。")
    
    # 4. 外部リンクボタン
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        google_link = f"https://www.google.com/maps/search/{encoded_query}"
        st.link_button("🌐 Googleマップアプリで開く", google_link, use_container_width=True)
    with col2:
        st.button("📋 検索履歴に保存（準備中）", use_container_width=True)
