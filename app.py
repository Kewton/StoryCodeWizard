import streamlit as st
from form.chat import chat
from form.regist_markdown import register_document
from form.edit_markdown import edit_markdown
from myjsondb.myStreamlit import MyStreamlitDo, MyStremalit

def main():
    st.sidebar.title("Navigation")

    myStreamlitDo = MyStreamlitDo()
    myStreamlitDo.formname = "main"
    myStreamlitDo.keyname = "form_menu"
    for a in MyStremalit.jsondb.getByQuery(myStreamlitDo.to_query_dict()):
        data = MyStreamlitDo().from_json_dict(a)
        _form_menu = data.value["form_menu"]
    selection = st.sidebar.radio("Go to", _form_menu)

    if selection == _form_menu[0]:
        chat(selection)
    elif selection == _form_menu[1]:
        register_document(selection)
    elif selection == _form_menu[2]:
        edit_markdown(selection)

if __name__ == '__main__':
    main()