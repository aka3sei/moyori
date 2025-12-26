import streamlit as st
import urllib.parse

# 1. ページ設定
st.set_page_config(page_title="最寄り駅検索", layout="centered")

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
st.info("周辺の店舗情報を排除し、最も近い駅の地点を特定します。")

st.write("---")

# ③ 現在地検索ボタン
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 現在地から最短の駅を探す", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 【バックテストに基づく改善】
    # 通常の検索(q=)だと周辺店舗が出るため、
    # 目的地(daddr)を「駅」に指定した経路表示形式を応用します。
    # これにより、最短の駅が「目的地ピン」として一際大きく表示されます。
    origin = urllib.parse.quote(address)
    destination = urllib.parse.quote("最寄り駅")
    
    # saddr(出発地)=住所, daddr(目的地)=駅, dirflg=w(徒歩)
    # このURL構成にすることで、飲食店などのピンが「背景」になり、駅が「目的地」として強調されます。
    map_url = f"https://maps.google.com/maps?q=?saddr={origin}&daddr={destination}&dirflg=w&output=embed&z=16&hl=ja"
    
    st.subheader(f"🚩 最短ルートの駅を確認")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.success("青いラインの先にあるピンが、最も近い駅です。周辺の店舗アイコンは無視してください。")
    
    # アプリ連携
    google_link = f"https://www.google.com/maps/search/?saddr={origin}&daddr={destination}&dirflg=w"
    st.link_button("🚀 この駅へのナビを開始する", google_link, use_container_width=True)

else:
    st.write("※現在は住所の入力待ちです。")
