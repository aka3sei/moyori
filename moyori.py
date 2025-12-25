import streamlit as st
import urllib.parse

# ページ設定
st.set_page_config(page_title="最寄り駅・周辺検索", layout="centered")

# ヘッダー非表示
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")
st.caption("Googleの最新データベースを使用して周辺駅を表示します")

# 1. 住所入力
address = st.text_input("住所や地名を入力してください", placeholder="例：新宿三丁目、三鷹市上連雀1")

if address:
    # Googleマップで「住所名 駅」で検索するURLを作成
    search_query = f"{address} 駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # Googleマップの検索結果を埋め込むURL
    # ※Google公式の検索表示機能を利用
    map_url = f"https://www.google.com/maps?q={encoded_query}&output=embed"
    
    st.subheader(f"📍 {address} 周辺の駅情報")
    
    # 2. Googleマップ（駅検索結果）を直接表示
    # これならAPI制限に関係なく、100%表示されます
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    
    st.success("上の地図内で、最寄り駅と徒歩ルートを確認できます。")
    
    # 3. 補足：ワンクリックでナビを開くボタン
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        google_link = f"https://www.google.com/maps/search/{encoded_query}"
        st.link_button("🌐 Googleマップアプリで開く", google_link, use_container_width=True)
    with col2:
        # リフォームアプリなど他のアプリへのリンク（必要に応じて）
        st.button("📋 検索履歴に保存（機能準備中）", use_container_width=True)

else:
    st.info("住所を入力してEnterを押すと、周辺の駅が地図上に一覧表示されます。")
