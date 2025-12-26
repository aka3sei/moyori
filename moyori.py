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

st.title("🚉 最寄り駅検索")

# ① 住所入力欄
address = st.text_input("住所や地名を入力してください", placeholder="例：西新宿1-26-2")

# ② 説明テキスト
st.info("入力された場所から「一番近い駅」を1つ特定して表示します。")

st.write("---")

# ③ 現在地検索ボタン
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 現在地から最短の駅を探す（アプリ）", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 【最短の1駅に絞る工夫】
    # 「nearest station」という英語キーワードを混ぜることで、
    # Googleが「複数候補」ではなく「最も近い1地点」を特定する確率が高まります。
    search_query = f"{address} nearest station" 
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURL
    # iwloc=A を指定し、最も関連度の高い（一番近い）場所の情報を強制的に開きます
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja&iwloc=A"
    
    st.subheader(f"🚩 最寄りの駅: {address} 付近")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.success("赤いピンが、入力地点から最も近いと思われる駅です。")
    
    # アプリ連携
    google_link = f"https://www.google.com/maps/search/{encoded_query}"
    st.link_button("🚀 この駅へのルートをアプリで確認", google_link, use_container_width=True)

else:
    st.write("※現在は住所の入力待ちです。")
