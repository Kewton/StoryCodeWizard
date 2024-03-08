import streamlit as st
from myjsondb.ragDocDb import RagDocDo, ragDB

def register_document(_title):
    st.title(_title)

    # テキストエリアウィジェット（マークダウン編集欄）
    data_set_mame = st.text_input("Data Set Name")
    data_set_Description = st.text_input("Data Set Description")

    # テキストエリアウィジェット（マークダウン編集欄）
    markdown_text = st.text_area("Edit Markdown", height=200)

    # プレビューエリア
    st.markdown("### Preview")
    st.markdown(markdown_text, unsafe_allow_html=True)

    # 更新ボタン
    if st.button("Save to Database"):
        ragdo = RagDocDo()
        ragdo.dataset_name = data_set_mame
        ragdo.dataset_description = data_set_Description
        ragdo.markdown_text = markdown_text
        ragDB.upsert(ragdo)
        st.success("Content saved to the database!")

