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
st.info("住所を入力してEnterを押すと、その場所と周辺の駅に目立つ印を表示します。")

st.write("---")

# ③ 現在地検索ボタン
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 現在地を特定してアプリで開く", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 【ここが重要】「住所 ＋ 駅」という組み合わせではなく
    # 「駅 near 住所」という特殊な形式にすることで、駅一つ一つに赤いピンが立ちやすくなります
    search_query = f"駅 near {address}"
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURL（駅に目立つマークをつけさせるため output=embed を使用）
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=15&hl=ja"
    
    st.subheader(f"📍 {address} 周辺の主要駅")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.success("地図上の目立つマークが駅です。クリックすると駅名が表示されます。")
    
    # アプリ連携ボタン
    google_link = f"https://www.google.com/maps/search/{encoded_query}"
    st.link_button("🚀 Googleマップアプリで大きな地図を見る", google_link, use_container_width=True)

else:
    st.write("※現在は検索待ちの状態です。")
