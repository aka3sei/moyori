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
    /* 現在地ボタンを強調 */
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
address = st.text_input("住所や地名を入力してください", placeholder="例：新宿三丁目、三鷹市野崎4-8")

# ② 説明テキスト
st.info("住所を入力してEnterを押すと、その地点にピンを立てて周辺駅を表示します。")

st.write("---")

# ③ 現在地検索ボタン（ここを押すと、スマホのGPSで「今いる点」が青く光るマップが開きます）
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 現在地を特定して地図アプリで開く", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 【工夫】キーワードに「駅」だけでなく「住所そのもの」を強調させるクエリ構成
    # これにより、入力した地点に赤いピンが落ちやすくなります
    search_query = f"{address}"
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURL（q=住所 にすることでピンを落とし、周辺の駅も自動で表示される設定）
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja"
    
    st.subheader(f"🚩 検索地点: {address}")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    
    st.success("赤いピンの場所が入力された住所です。周辺の駅アイコンをクリックすると詳細が見れます。")
    
    # アプリ連携ボタン
    google_link = f"https://www.google.com/maps/search/{encoded_query}+最寄り駅"
    st.link_button("🚀 Googleマップアプリでルートを確認", google_link, use_container_width=True)

else:
    # 住所未入力時のプレースホルダー（現在地の目安として三鷹を表示）
    st.write("※現在は検索待ちの状態です。")
