import streamlit as st
from myjsondb.ragDocDb import RagDocDo, ragDB

def edit_markdown(_title):
    st.title(_title)

    datasets = ragDB.jsondb.getAll()

    option = []
    for a in datasets:
        data = RagDocDo().from_json_dict(a)
        option.append(data.dataset_name)

    selected_option = st.selectbox("Choose an option", option)
    st.write(f"{selected_option} の詳細内容を確認する")
    
    _description = ""
    _markdown_text = ""
    _markdown_text = ""
    for a in datasets:
        data = RagDocDo().from_json_dict(a)
        if data.dataset_name == selected_option:
            _description = data.dataset_description
            _markdown_text = data.markdown_text

    data_set_Description = st.text_input("Data Set Description", _description)

    markdown_text = st.text_area("Markdownを編集", _markdown_text, height=300)

    # ユーザーが入力したMarkdownをプレビュー
    st.markdown("## Preview")
    st.markdown(markdown_text, unsafe_allow_html=True)
    # 更新ボタン
    if st.button("Update"):
        ragdo = RagDocDo()
        ragdo.dataset_name = selected_option
        ragdo.dataset_description = data_set_Description
        ragdo.markdown_text = markdown_text
        ragDB.upsert(ragdo)

        st.success("Content saved to the database!")
        