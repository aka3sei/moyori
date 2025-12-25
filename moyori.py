import streamlit as st
import urllib.parse

# ページ設定
st.set_page_config(page_title="最寄り駅・周辺検索", layout="wide")

# デザイン調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; }
    .block-container { padding-top: 1rem; }
    /* 地図の角を丸くする */
    iframe { border-radius: 10px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

st.title("🚉 最寄り駅・周辺検索")
st.caption("Googleマップと連携し、全国の駅名と経路を確実に表示します")

# 1. 住所入力
address = st.text_input("住所や地名を入力してください（例：三鷹市上連雀1丁目、新宿三丁目）", placeholder="ここに入力してEnter")

if address:
    # Google検索用のクエリ作成
    search_query = f"{address} 駅"
    encoded_query = urllib.parse.quote(search_query)
    
    # 2カラムレイアウトで「リスト」と「地図」を並べる
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("📋 周辺駅の確認")
        st.write(f"「{address}」周辺には以下の駅があります。詳細は地図内のピンをタップしてください。")
        
        # 簡易的な案内（Googleマップへの誘導）
        st.info("💡 地図上の「駅アイコン」をクリックすると、駅名と路線名、ここからの徒歩ルートが詳しく表示されます。")
        
        # 外部リンクボタン
        google_link = f"https://www.google.com/maps/search/{encoded_query}"
        st.link_button("🌐 大きな地図で確認（Googleマップ）", google_link, use_container_width=True)
        
        # おまけ：不動産用メモ
        st.text_area("物件メモ", placeholder="例：三鷹駅 徒歩12分、駐輪場あり", height=150)

    with col_right:
        st.subheader(f"📍 周辺マップ")
        # Googleマップの埋め込み（output=embed を使用）
        # z=15 はズームレベル（15〜16が駅周辺を見るのに最適）
        map_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed&z=15&hl=ja"
        
        st.components.v1.iframe(map_url, height=550, scrolling=True)

    st.success("検索が完了しました。地図を動かして周辺環境（コンビニ・スーパー等）も確認できます。")

else:
    st.info("住所を入力してEnterを押すと、駅名と地図が表示されます。")
