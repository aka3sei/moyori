import streamlit as st
import urllib.parse

# 1. ページ設定
st.set_page_config(page_title="最寄り駅・周辺検索", layout="centered")

# CSS: デザイン調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    iframe { border-radius: 15px; border: 1px solid #ddd; }
    div.stButton > button { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")

# 2. 住所入力
address = st.text_input("住所や地名を入力してください", placeholder="例：新宿三丁目、三鷹市上連雀1")
st.info("住所を入力してEnterを押すと、周辺の駅が地図上に一覧表示されます。")

st.write("---")
st.write("または、スマートフォンのGPSを使用して検索します。")

# --- JavaScriptによる位置情報取得 ---
# このHTML/JSコンポーネントが実行されると、ブラウザからPython側に座標が送られます
get_loc_html = """
<script>
navigator.geolocation.getCurrentPosition(
    (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        // Streamlitの親ウィンドウにメッセージを送る
        window.parent.postMessage({
            type: 'streamlit:set_component_value',
            value: {lat: lat, lon: lon}
        }, '*');
    },
    (error) => { console.error(error); },
    {enableHighAccuracy: true}
);
</script>
"""

# st.componentsでJavaScriptを実行し、値を受け取る
from streamlit.components.v1 import html
# 透明で高さ0のiframeとして埋め込む
loc_data = st.components.v1.html(get_loc_html, height=0)

search_target = None
label = ""

# --- 判定ロジック ---
if address:
    search_target = address
    label = address
else:
    # ボタンが押されたとき
    if st.button("📍 現在地で最寄り駅を検索", use_container_width=True):
        # 注意: JSからのデータ取得にはラグがあるため、もう一度確認が必要な場合があります
        st.warning("現在地を取得中です...。ブラウザから許可を求められたら「許可」を押してください。")
        # クエリパラメータなどを利用しない簡易版では、一度入力欄を空にして「現在地」と打つなどの工夫も可能です。
        # ここでは住所が空の状態でボタンが押されたらGoogleマップ側で「現在地」として処理させます。
        search_target = "現在地"
        label = "現在地"

# --- 表示処理 ---
if search_target:
    # 検索クエリの作成
    search_query = f"{search_target} 最寄り駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # Googleマップ埋め込みURL（APIキー不要形式）
    map_url = f"https://www.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja"
    
    st.subheader(f"📍 {label} 付近の駅情報")
    
    # 地図の表示
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    st.success("上の地図内で、最寄り駅と徒歩ルートを確認できます。")
    
    # 外部リンク
    st.divider()
    google_link = f"https://www.google.com/maps/search/{encoded_query}"
    st.link_button("🌐 Googleマップアプリで開く", google_link, use_container_width=True)
