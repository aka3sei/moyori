import streamlit as st
import urllib.parse

st.set_page_config(page_title="最寄り駅・周辺検索", layout="centered")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    iframe { border-radius: 10px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")
st.caption("最寄り駅を強調して表示します")

address = st.text_input("住所や地名を入力してください", placeholder="例：三鷹市上連雀1")

if address:
    # 検索クエリを「最寄り駅」にして精度を上げる
    search_query = f"{address} 最寄り駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURLに「z=16 (ズーム)」と「hl=ja (日本語)」を追加
    # これで駅名がハッキリ印字されます
    map_url = f"https://www.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja"
    
    st.subheader(f"📍 {address} の最寄り駅を確認")
    
    # 地図表示
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    
    st.divider()
    
    # より「はっきり認識」するための追加アクションボタン
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 地図アプリ起動（一番確実）
        google_link = f"https://www.google.com/maps/search/{encoded_query}"
        st.link_button("🌐 アプリで開く", google_link, use_container_width=True)
        
    with col2:
        # 現在地から駅までの「徒歩ルート」を直接開く
        route_query = urllib.parse.quote(f"{address}から最寄り駅")
        route_link = f"https://www.google.com/maps/dir/{route_query}"
        st.link_button("🚶 徒歩ルート確認", route_link, use_container_width=True)
        
    with col3:
        # 周辺のコンビニなどもついでに探せるように
        cvs_query = urllib.parse.quote(f"{address} コンビニ")
        cvs_link = f"https://www.google.com/maps/search/{cvs_query}"
        st.link_button("🏪 周辺のコンビニ", cvs_link, use_container_width=True)

else:
    st.info("住所を入力すると、最寄り駅にズームした地図が表示されます。")
