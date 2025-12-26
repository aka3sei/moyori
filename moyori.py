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
address = st.text_input("住所や地名を入力してください", placeholder="例：三鷹市野崎4-8")

# ② 説明テキスト
st.info("住所を入力してEnterを押すと、その場所に赤いピンを立て、周辺の駅を強調表示します。")

st.write("---")

# ③ 現在地検索ボタン（スマホアプリ連動用）
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 今いる場所を正確に特定（アプリ起動）", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 【最重要】現在地（住所）を確定させつつ、周辺の駅を呼び出す特殊なクエリ
    # 「住所」を先に書き、その後に「駅」を足すことで、住所に赤いピンが立ちやすくなります
    search_query = f"loc:{address} 駅" 
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURL（z=15 で少し広めに見せて駅を見つけやすくします）
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=15&hl=ja"
    
    st.subheader(f"🚩 検索地点と周辺駅: {address}")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.markdown("""
    **地図の見方：**
    - 🚩 **赤いピン**：入力した住所（現在地）
    - 🚉 **駅アイコン**：周辺の駅（クリックで駅名が表示されます）
    """)
    
    # アプリ連携ボタン
    google_link = f"https://www.google.com/maps/search/{encoded_query}"
    st.link_button("🚀 Googleマップアプリでルート案内を開始", google_link, use_container_width=True)

else:
    st.write("※現在は検索待ちの状態です。")
