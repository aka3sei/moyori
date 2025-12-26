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
address = st.text_input("住所や地名を入力してください", placeholder="例：西新宿１丁目、西新宿1-26-2")

# ② 説明テキスト
st.info("入力された住所の周辺にある『駅・バス停』を強調して表示します。")

st.write("---")

# ③ 現在地検索ボタン
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 現在地を特定してアプリで開く", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 【ここが解決の鍵】
    # 番地が入っても「周辺の駅」という言葉を足すことで、
    # 西新宿1丁目と入力したときと同じ「駅・バス停強調モード」を強制します。
    search_query = f"{address} 周辺の駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURL（駅のマーカーを表示させる設定）
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=15&hl=ja"
    
    st.subheader(f"📍 {address} 付近の公共交通機関")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.success("地図上のピンは周辺の駅やバス停を示しています。")
    
    # アプリ連携
    google_link = f"https://www.google.com/maps/search/{encoded_query}"
    st.link_button("🚀 Googleマップアプリで詳細を見る", google_link, use_container_width=True)

else:
    st.write("※現在は住所の入力待ちです。")
