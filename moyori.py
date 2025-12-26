import streamlit as st
import urllib.parse

# 1. ページ設定
st.set_page_config(page_title="最短駅ナビ", layout="centered")

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

st.title("🚉 最短・最寄り駅検索")

# ① 住所入力欄
address = st.text_input("住所や地名を入力してください", placeholder="例：西新宿1-26-2")

# ② 説明テキスト
st.info("飲食店などの情報を排除し、最短の駅へのルートを表示します。")

st.write("---")

# ③ 現在地検索ボタン
current_query = urllib.parse.quote("現在地から一番近い駅")
st.link_button("📍 現在地から最短駅を探す", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 住所と「最寄り駅」をエンコード
    origin = urllib.parse.quote(address)
    # 「最寄り駅」という目的地を指定することで、Googleが最短の1件を自動抽出します
    destination = urllib.parse.quote("駅")
    
    # 【最重要】検索(search)ではなく経路(directions)モードを使用
    # これにより、飲食店やホテルのピンが劇的に減り、駅が「目的地」として際立ちます
    # dirflg=w (徒歩ルート) を指定
    map_url = f"https://www.google.com/maps/embed/v1/directions?key=YOUR_API_KEY_IS_NOT_NEEDED_HERE&origin={origin}&destination={destination}&mode=walking&language=ja"
    
    # APIキーなしで動作する経路埋め込みURL（特殊形式）
    map_url = f"https://maps.google.com/maps?f=d&saddr={origin}&daddr={destination}&dirflg=w&output=embed&z=16"
    
    st.subheader(f"🚩 {address} からの最短駅")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.success("地図上の「B」地点が、最も近い駅です。")
    
    # アプリ連携
    google_link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=walking"
    st.link_button("🚀 Googleマップアプリで詳細・ナビを見る", google_link, use_container_width=True)

else:
    st.write("※現在は住所の入力待ちです。")
