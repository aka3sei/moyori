import streamlit as st

st.title("テスト中：反映確認用")
st.write("これが表示されていれば、最新のコードが読み込まれています。")

# 入力欄
address = st.text_input("住所入力")

# 説明テキスト（ここに表示されるはず）
st.info("住所を入力してEnterを押すと、周辺の駅が表示されます。")

if address:
    st.write(f"入力された住所: {address}")
