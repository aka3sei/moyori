import streamlit as st
import urllib.parse

# 1. ページ設定
st.set_page_config(page_title="最寄り駅・周辺検索", layout="centered")

# デザイン調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    iframe { border-radius: 15px; border: 2px solid #1a73e8; }
    .stLinkButton > a {
        background-color: #f0f2f6 !important;
        border: 2px solid #1a73e8 !important;
        color: #1a73e8 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")

# ① 住所入力欄
address = st.text_input("住所や地名を入力してください", placeholder="例：三鷹市大沢2丁目")

# ② 説明テキスト
st.info("住所を入力してEnterを押すと、その場所に赤いピンが立ちます。周辺の駅アイコンも表示されます。")

st.write("---")

# ③ 現在地検索ボタン
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 現在地を特定してアプリで開く", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 住所のみをクエリにすることで、確実に赤いピン（マーカー）を立てます
    encoded_query = urllib.parse.quote(address)
    
    # 埋め込みURL
    # z=15 に設定。住所のピンを出しつつ、近くの駅アイコンが画面内に入る距離感です。
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=15&hl=ja"
    
    st.subheader(f"🚩 検索地点: {address}")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.success("赤いピンの場所が入力された住所です。")
    
    # 【追加】駅が目立たない場合の補足として、アプリへのリンクを「駅検索モード」で作成
    station_query = urllib.parse.quote(f"{address} 最寄り駅")
    google_link = f"https://www.google.com/maps/search/{station_query}"
    st.link_button("🔍 この場所の『最寄り駅』をアプリで詳しく見る", google_link, use_container_width=True)

else:
    st.write("※現在は検索待ちの状態です。")
