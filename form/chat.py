import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
from secret_keys import openai_api_key
from myjsondb.myStreamlit import MyStreamlitDo, MyStremalit
import os

load_dotenv()

client = OpenAI(
  api_key=openai_api_key
)


def fetch_packagejson_and_contents():
    all_files = []
    # ファイルを開き、内容を読み込む
    try:
        with open("./front/package.json", 'r', encoding='utf-8') as file:
            content = file.read().replace('"', '\\"')
            all_files.append("- filename:./front/package.json")
            all_files.append("\\`\\`\\`")
            all_files.append(content)
            all_files.append("\\`\\`\\`")
            all_files.append("")
    except (UnicodeDecodeError, IOError):
        print("Error reading ./front/package.json. It may not be a text file or might have encoding issues.")
    return '\n'.join(str(elem) for elem in all_files)

def fetch_files_and_contents(directory):
    all_files = []
    
    # os.walk()を使用してディレクトリを再帰的に走査
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if ".DS_Store" != filename:
                # ファイルの完全なパスを取得
                file_path = os.path.join(root, filename)
                
                # ファイルを開き、内容を読み込む
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read().replace('"', '\\"')
                        all_files.append(f"- filename:{file_path}")
                        all_files.append("\\`\\`\\`")
                        all_files.append(content)
                        all_files.append("\\`\\`\\`")
                        all_files.append("")
                except (UnicodeDecodeError, IOError):
                    print(f"Error reading {file_path}. It may not be a text file or might have encoding issues.")

    return '\n'.join(str(elem) for elem in all_files) 


# チャットボットとやりとりする関数
def communicate(_selected_response_format, _selected_model, selected_programing_model):
    messages = st.session_state["messages"]
    request_messages = []
    

    if "normal" == _selected_response_format:
        myStreamlitDo = MyStreamlitDo()
        myStreamlitDo.formname = "chat"
        myStreamlitDo.keyname = "systemrole"
        for a in MyStremalit.jsondb.getByQuery(myStreamlitDo.to_query_dict()):
            data = MyStreamlitDo().from_json_dict(a)
            _systemrole_content = data.value[selected_programing_model]


        #print("@_systemrole_content")
        #print(_systemrole_content)
        #print("@st.session_state")
        #print(st.session_state["user_input"])
        messages.append({"role": "system", "content": st.session_state["user_input"]})
        request_messages.append({"role": "system", "content": _systemrole_content[0]})

        _content = f"""
        前提と現在のソースコードと要求と制約から最高の成果物を生成してください。
 
        # 前提
        -'./front'ディレクトリにてNext.jsのフロントエンドを開発しています

        # 制約
        - 新規にインストールが必要なライブラリを明確にすること
        - 新規に作成が必要なファイル名を明確にすること
        - 各コンポーネントの全体における位置付けを明確にすること

        # 要求
        {st.session_state["user_input"]}

        # 現在のpackage.json
        {fetch_packagejson_and_contents()}

        # 現在のソースコード
        {fetch_files_and_contents("./front/src")}
        """

        #print(_content)

        user_message = {"role": "user", "content": _content}
        request_messages.append(user_message)

        #print("-------")
        #print("-------")
        #print(messages[1])
        response = client.chat.completions.create(
            model=_selected_model,
            messages=request_messages
        )
    else:
        messages.append({"role": "system", "content": "あなたは返答をすべてJSON形式で出力します。"})
        messages.append({"role": "user", "content": st.session_state["user_input"]})
        response = client.chat.completions.create(
            model=_selected_model, 
            response_format={"type":_selected_response_format},
            messages=messages
        )

    bot_message = {
        "content": response.choices[0].message.content,
        "role": response.choices[0].message.role
    }
        
    messages.append(bot_message)

def session_control(_selected_response_format, _selected_model, selected_programing_model):
    
    communicate(_selected_response_format, _selected_model, selected_programing_model)
    st.session_state["user_input"] = ""  # 入力欄を消去

def chat(_title):

    # st.session_stateを使いメッセージのやりとりを保存
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
            ]

    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""

    # ユーザーインターフェイスの構築
    st.title(_title)

    st.write("ChatGPT APIを使ったチャットボットです。")

    messages = st.session_state["messages"]
    for message in messages[1:]:  # 直近のメッセージを上に
        speaker = "<you>🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

    selected_response_format = st.selectbox("Choose Response format", ("normal", "json_object"), key="selected_response_format")

    myStreamlitDo = MyStreamlitDo()
    myStreamlitDo.formname = "chat"
    myStreamlitDo.keyname = "gpt"
    for a in MyStremalit.jsondb.getByQuery(myStreamlitDo.to_query_dict()):
        data = MyStreamlitDo().from_json_dict(a)
        _model_menu = data.value["gpt_model"]
    selected_model = st.selectbox("Choose Gpt Model", tuple(_model_menu), key="selected_model")


    myStreamlitDo = MyStreamlitDo()
    myStreamlitDo.formname = "chat"
    myStreamlitDo.keyname = "systemrole"
    for a in MyStremalit.jsondb.getByQuery(myStreamlitDo.to_query_dict()):
        data = MyStreamlitDo().from_json_dict(a)
        _programing_language = data.value["プログラミング言語"]
    selected_programing_model = st.selectbox("Choose Programing Language", tuple(_programing_language), key="selected_programing_language")


    user_input = st.text_area("メッセージを入力してください。", key="user_input", value=st.session_state["user_input"])
    submit_button = st.button("Submit", on_click=session_control,args=(selected_response_format,selected_model,selected_programing_model, ))
