import streamlit as st

# 1. ページ設定
st.set_page_config(page_title="最寄り駅・周辺検索", layout="centered")

# CSS: ボタンを大きく押しやすく
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    div.stButton > button {
        height: 100px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        background-color: #1a73e8 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")

# --- JavaScriptでデバイスのGPS（緯度・経度）を直接取得 ---
# これにより通信拠点ではなく、端末の現在地を1メートル単位で特定します
get_location_script = """
<script>
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      // Googleマップの検索URL（目的地を「最寄り駅」に設定）
      const url = `https://www.google.com/maps/search/?api=1&query=${lat},${lon}+最寄り駅`;
      window.open(url, '_blank');
    }, function(error) {
      alert("位置情報の取得に失敗しました。設定からブラウザの位置情報を許可してください。");
    }, {enableHighAccuracy: true});
  } else {
    alert("お使いのブラウザはGPSに対応していません。");
  }
}
</script>
<button onclick="getLocation()" style="
    width: 100%;
    height: 100px;
    background-color: #1a73e8;
    color: white;
    border: none;
    border-radius: 20px;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
">📍 現在地で最寄り駅を検索</button>
"""

st.write("下のボタンを押すと、スマホのGPSを使用して正確な現在地を特定し、付近の駅を表示します。")

# JavaScriptのボタンを表示
st.components.v1.html(get_location_script, height=120)

st.write("---")

# 手動入力用
st.subheader("住所で検索する場合")
address = st.text_input("住所や地名を入力", placeholder="例：新宿三丁目")
if address:
    import urllib.parse
    query = urllib.parse.quote(f"{address} 最寄り駅")
    st.link_button(f"🔍 {address} 周辺の駅を検索", f"https://www.google.com/maps/search/?api=1&query={query}")

st.info("※ボタンを押した際、「位置情報の使用を許可しますか？」と表示されたら必ず「許可」を選択してください。")
