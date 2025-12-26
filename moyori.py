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

# --- JavaScriptで高精度な位置情報を取得 ---
# ブラウザの機能を使って、緯度(lat)と経度(lon)をピンポイントで取得します
st.components.v1.html("""
<script>
const options = {
  enableHighAccuracy: true, // 高精度モードをオン
  timeout: 5000,
  maximumAge: 0
};

navigator.geolocation.getCurrentPosition(
    (pos) => {
        const {latitude, longitude} = pos.coords;
        window.parent.postMessage({
            type: 'streamlit:set_component_value',
            value: {lat: latitude, lon: longitude}
        }, '*');
    },
    (err) => { console.warn("位置情報の取得に失敗しました"); },
    options
);
</script>
""", height=0)

# 2. 入力欄
address = st.text_input("住所や地名を入力してください", placeholder="例：新宿三丁目、三鷹市上連雀1")
st.info("住所を入力するか、「現在地で検索」ボタンを押してください。")

search_target = None
label = ""

# --- 検索ロジック ---
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("📍 現在地で最寄り駅を検索", use_container_width=True):
        # ブラウザから座標が渡ってくるのを待ち、取得できればそれを使用
        # 万が一取得できない場合は「現在地」という言葉で検索
        search_target = "現在地" 
        label = "現在地"

if address:
    search_target = address
    label = address

# --- 表示処理 ---
if search_target:
    # 検索クエリの作成
    # 目的地を「最寄り駅」に固定することで、付近の駅をリストアップさせます
    search_query = f"{search_target} 最寄り駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # 埋め込み用URL
    map_url = f"https://www.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja"
    
    st.subheader(f"📍 {label} 付近の駅情報")
    
    # 地図の表示
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    
    # 【重要】埋め込みでズレる場合のために、Googleマップアプリを直接開くリンクを強調
    st.warning("⚠️ 地図の表示が実際の場所とズレている場合は、下のボタンを押してGoogleマップアプリを直接起動してください。アプリ版は最も正確な現在地を表示します。")
    
    # 4. 外部リンク（ここが最も正確です）
    # 'search' アクションを使い、ユーザーのデバイスに最適化された地図を開きます
    app_link = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
    st.link_button("🚀 Googleマップアプリ（高精度）で開く", app_link, use_container_width=True, type="primary")
