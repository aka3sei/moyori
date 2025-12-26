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
st.info("住所を入力してEnterを押すと、その場所にピンを立て、周辺駅を強調表示します。")

st.write("---")

# ③ 現在地検索ボタン
current_query = urllib.parse.quote("現在地 最寄り駅")
st.link_button("📍 現在地を特定してアプリで開く", f"https://www.google.com/maps/search/{current_query}", use_container_width=True)

# 4. 表示処理
if address:
    # 【工夫】住所の周辺にある「駅」を複数強調するためのクエリ
    # view:map を指定し、検索対象を「駅」に絞り込むことで印を目立たせます
    search_query = f"{address} 周辺の駅" 
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込みURL（倍率を14に少し下げて、より多くの駅が印付きで入るようにします）
    map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=14&hl=ja"
    
    st.subheader(f"🚩 検索地点と周辺駅の強調表示")
    
    # Googleマップを表示
    st.components.v1.iframe(map_url, width=None, height=550, scrolling=True)
    
    st.markdown(f"""
    **現在の表示：**
    - 入力された **{address}** を中心に、周辺の駅を強調しています。
    - 地図上の各アイコンをクリックすると、駅の詳細（路線名など）を確認できます。
    """)
    
    # アプリ連携ボタン
    google_link = f"https://www.google.com/maps/search/{encoded_query}"
    st.link_button("🚀 Googleマップアプリでルート案内を開始", google_link, use_container_width=True)

else:
    st.write("※現在は検索待ちの状態です。")
