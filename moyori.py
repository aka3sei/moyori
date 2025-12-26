import streamlit as st
import urllib.parse

# 1. ページ設定
st.set_page_config(page_title="最寄り駅・周辺検索", layout="centered")

# ヘッダー非表示・余白調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    /* 地図の角を丸くする */
    iframe { border-radius: 15px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")

# 2. 住所入力
address = st.text_input("住所や地名を入力してください", placeholder="例：新宿三丁目、三鷹市上連雀1")

if address:
    # 検索クエリの作成
    search_query = f"{address} 最寄り駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURLの設定（ズームレベル16、日本語表示）
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja"
    
    st.subheader(f"📍 {address} 付近の駅情報")
    
    # 3. Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    
    st.success("上の地図内で、最寄り駅を確認できます。")
    
    # 4. 外部リンクボタン
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        # 確実に現在地から検索できるよう、Googleマップ公式へのリンク
        google_link = f"https://www.google.com/maps/search/{encoded_query}"
        st.link_button("🌐 Googleマップアプリで開く", google_link, use_container_width=True)
    with col2:
       
else:
    st.info("住所を入力してEnterを押すと、周辺の駅が地図上に表示されます。")
    
    # 初期状態では「現在地」で検索するボタンをシンプルに配置
    current_query = urllib.parse.quote("現在地 最寄り駅")
    st.link_button("📍 今いる場所で検索（アプリ起動）", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

