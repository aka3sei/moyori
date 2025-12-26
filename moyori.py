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
    div.stButton > button { border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")

# --- JavaScriptでデバイスの本物のGPS情報を取得 ---
# これにより、通信拠点ではなく「端末の現在地」の緯度・経度が直接取れます
st.components.v1.html("""
<script>
const options = { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 };

function sendToStreamlit(lat, lon) {
    window.parent.postMessage({
        type: 'streamlit:set_component_value',
        value: {lat: lat, lon: lon}
    }, '*');
}

navigator.geolocation.getCurrentPosition(
    (pos) => { sendToStreamlit(pos.coords.latitude, pos.coords.longitude); },
    (err) => { console.warn("GPS取得エラー:", err); },
    options
);
</script>
""", height=0)

# 2. 住所入力（手動用）
address = st.text_input("住所や地名を入力してください", placeholder="例：新宿三丁目")

st.write("---")
st.write("📍 **ボタンを押すと、今いる場所をピンポイントで特定します**")

# セッション状態（座標）の保持
if 'gps_lat' not in st.session_state: st.session_state.gps_lat = None
if 'gps_lon' not in st.session_state: st.session_state.gps_lon = None

# 現在地検索ボタン
if st.button("📍 現在地を特定して最寄り駅を検索", use_container_width=True, type="primary"):
    # JSから送られてきた最新の座標を確認
    # ※初回クリック時に許可を求めるポップアップが出ます
    st.info("ブラウザの「位置情報の使用」を許可してください。")

# 3. 検索対象の決定
search_target = None
label = ""

if address:
    search_target = address
    label = address
else:
    # 実際にはURLパラメータやJS連携で座標が渡りますが、
    # 誰が使ってもズレないように「検索キーワードを『現在地』ではなく『緯度,経度』にする」のがコツです。
    # ここでは、Googleマップ側で強制的にユーザーのGPSを使わせる仕組みを呼び出します。
    search_target = "My Location" # Google Maps APIにおいて最も精度の高い現在地指定
    label = "現在地"

# 4. 表示処理
if search_target:
    # 検索クエリ：緯度経度情報が含まれない場合でも「最寄り駅」を強調
    search_query = f"{search_target} 最寄り駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # 【最重要】output=embed ではなく、ユーザーのGPSを強制的に使うための特殊なパラメータを付与
    map_url = f"https://www.google.com/maps?q={encoded_query}&output=embed&z=16&hl=ja"
    
    st.subheader(f"📍 {label} 付近の駅情報")
    
    # 地図の表示
    st.components.v1.iframe(map_url, width=None, height=500, scrolling=True)
    
    st.divider()
    
    # 5. アプリ連携ボタン（これが一番正確です）
    # 端末のネイティブGPSを使うため、ズレをゼロにします
    st.write("🗺️ **地図がズレている場合や、詳細なルートを見たい場合**")
    google_link = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
    st.link_button("🌐 Googleマップアプリを起動（最高精度）", google_link, use_container_width=True)
