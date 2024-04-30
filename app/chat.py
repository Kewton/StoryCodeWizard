import streamlit as st
import os
from openai import OpenAI
from secret_keys import openai_api_key
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName
from app.myjsondb.myStreamlit import upsertValueByFormnameAndKeyName, getValueListByFormnameAndKeyName

client = OpenAI(
  api_key=openai_api_key
)

# sesson state key
SS_USER_INPUT = "user_input"
SS_MESSAGES = "messages"

IGNORE_FILE_LIST = [
    ".DS_Store"
]

def escape(_instr):
    return _instr.replace('"', '\\"').replace('`', '\\`')


def fetch_packagejson_and_contents():
    # ファイルを開き、内容を読み込む
    try:
        all_files = []
        outstr = ""
        with open("./front/package.json", 'r', encoding='utf-8') as file:
            content = file.read()
            all_files.append("- filename:./front/package.json")
            all_files.append("```")
            all_files.append(content)
            all_files.append("```")
            all_files.append("")
        outstr = '\n'.join(str(elem) for elem in all_files)
        return outstr
    except (UnicodeDecodeError, IOError):
        print("Error reading ./front/package.json. It may not be a text file or might have encoding issues.")
        return "", ""


def fetch_files_and_contents(directory):
    all_files = []
    outstr = ""
    # os.walk()を使用してディレクトリを再帰的に走査
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename not in IGNORE_FILE_LIST:
                # ファイルの完全なパスを取得
                file_path = os.path.join(root, filename)
                
                # ファイルを開き、内容を読み込む
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        all_files.append(f"- filename:{file_path}")
                        all_files.append("```")
                        all_files.append(content)
                        all_files.append("```")
                        all_files.append("")
                except (UnicodeDecodeError, IOError):
                    print(f"Error reading {file_path}. It may not be a text file or might have encoding issues.")
    outstr = '\n'.join(str(elem) for elem in all_files)
    return outstr


def createPromt(_prerequisites, _input, _src_root_path):
    _content = f"""
    前提と現在のソースコードと要求と制約から最高の成果物を生成してください。

    # 前提
    {_prerequisites}

    # 制約
    - 新規にインストールが必要なライブラリを明確にすること
    - 新規に作成が必要なファイル名を明確にすること
    - UIの構成要素を言語化し、各コンポーネントの全体における位置付けを明確にすること

    # 要求
    {_input}

    # 現在のpackage.json
    {fetch_packagejson_and_contents()}

    # 現在のソースコード
    {fetch_files_and_contents(_src_root_path)}
    """
    return _content


# チャットボットとやりとりする関数
def communicate(_selected_model, selected_programing_model):
    messages = st.session_state[SS_MESSAGES]
    request_messages = []
    
    # messages.append({"role": "system", "content": st.session_state[SS_USER_INPUT]})

    _systemrole_content = getValueByFormnameAndKeyName("chat", "systemrole", selected_programing_model)        
    request_messages.append({"role": "system", "content": _systemrole_content["system_role"]})

    _content = createPromt(
        _systemrole_content["prerequisites"],
        st.session_state[SS_USER_INPUT],
        _systemrole_content["srcdire"])
    user_message = {"role": "user", "content": _content}
    request_messages.append(user_message)

    response = client.chat.completions.create(
        model=_selected_model,
        messages=request_messages
    )

    bot_message = {
        "content": response.choices[0].message.content,
        "role": response.choices[0].message.role
    }
        
    messages.append(bot_message)
    request_messages.append(bot_message)

    return request_messages


def session_control(_selected_model, selected_programing_model):
    print("-- 21 --")
    request_messages = communicate(_selected_model, selected_programing_model)
    upsertValueByFormnameAndKeyName("chat", "history",
                                    {
                                        "test":request_messages
                                    })
    st.session_state["user_input"] = ""  # 入力欄を消去
    return


def init_session():
    if SS_USER_INPUT not in st.session_state:
        st.session_state[SS_USER_INPUT] = ""

    # st.session_stateを使いメッセージのやりとりを保存
    if SS_MESSAGES not in st.session_state:
        st.session_state[SS_MESSAGES] = [
            {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
           ]


def buildChatMessageFromSession(_key):
    if "" == _key:
        messages = st.session_state[SS_MESSAGES]
    elif None == _key:
        messages = st.session_state[SS_MESSAGES]
    else:
        messages = getValueByFormnameAndKeyName("chat", "history", _key)

    for message in messages[1:]:  # 直近のメッセージを上に
        speaker = "<you>🙂"
        if message["role"] == "assistant":
            speaker = "<Agent>🤖"

        st.write(speaker + ": " + message["content"])


def getModelList():
    return tuple(getValueByFormnameAndKeyName("chat", "gpt", "gpt_model"))


def getProgramingLanguage():
    return tuple(getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語"))


def mainui(_title, _key):
    print("-- 11 --")
    # ユーザーインターフェイスの構築
    st.title(_title)

    st.write("ChatGPT APIを使ったチャットボットです。")

    init_session()

    buildChatMessageFromSession(_key)

    selected_model = st.selectbox(
        "Choose Gpt Model",
        getModelList(),
        key="selected_model")

    selected_programing_model = st.selectbox(
        "Choose Programing Language",
        getProgramingLanguage(),
        key="selected_programing_language")

    st.text_area(
        "メッセージを入力してください。",
        key="user_input",
        value=st.session_state[SS_USER_INPUT])

    print("-- 12 --")
    st.button(
        "Submit",
        on_click=session_control,
        args=(
            selected_model,
            selected_programing_model,)
        )


def chat(_title):
    print("-- 01 --")
    st.sidebar.title("History")
    selected_page = st.sidebar.selectbox("Choose a page:", getValueListByFormnameAndKeyName("chat", "history"))
    mainui(_title, selected_page)
