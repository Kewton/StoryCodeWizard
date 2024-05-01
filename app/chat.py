import streamlit as st
import os
from openai import OpenAI
from secret_keys import openai_api_key
import pandas as pd
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName
from app.myjsondb.myHistory import getValByKey, upsertValByKey, getAllHistory, deleteByKey

client = OpenAI(
  api_key=openai_api_key
)

# sesson state key
SS_USER_INPUT = "user_input"
SS_MESSAGES = "messages"


def escape(_instr):
    return _instr.replace('"', '\\"').replace('`', '\\`')


def fetch_packagejson_and_contents():
    # ファイルを開き、内容を読み込む
    try:
        all_files = []
        outstr = ""
        with open("./front/package.json", 'r', encoding='utf-8') as file:
            content = file.read()
            all_files.append(" - filename:./front/package.json")
            all_files.append("```json")
            all_files.append(content)
            all_files.append("```")
            all_files.append("")
        outstr = '\n'.join(str(elem) for elem in all_files)
        return outstr
    except (UnicodeDecodeError, IOError):
        print("Error reading ./front/package.json. It may not be a text file or might have encoding issues.")
        return "", ""


def fetch_files_and_contents(directory, ignorelist):
    all_files = []
    outstr = ""
    # os.walk()を使用してディレクトリを再帰的に走査
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename not in ignorelist:
                # ファイルの完全なパスを取得
                file_path = os.path.join(root, filename)

                # ファイルを開き、内容を読み込む
                try:
                    # 拡張子を取得
                    _, file_extension = os.path.splitext(file_path)
                    file_extension = file_extension.lstrip('.')
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        all_files.append(f" - filename:{file_path}")
                        all_files.append(f"```{file_extension}")
                        all_files.append(content)
                        all_files.append("```")
                        all_files.append("")
                except (UnicodeDecodeError, IOError):
                    print(f"Error reading {file_path}. It may not be a text file or might have encoding issues.")
    outstr = '\n'.join(str(elem) for elem in all_files)
    return outstr


def createPromt(_prerequisites, _input, _src_root_path, _ignorelist):
    _content = f"""
# 命令指示書
- 前提と現在のソースコードと要求と制約から最高の成果物を生成してください。

### 前提
{_prerequisites}

### 制約
- アウトプットはmarkdown形式とすること
- 要求文書を適切な表現に変換すること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- 新規にインストールが必要な場合、ライブラリのインストール方法を明確にすること
- 新規にファイル作成が必要な場合、名称と拡張子も明確にしソースコードをフルで出力すること
- git への commit コメントを出力すること

### 要求
{_input}

### 現在のpackage.json
{fetch_packagejson_and_contents()}

### 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
    return _content


# チャットボットとやりとりする関数
def communicate(_selected_model, selected_programing_model):
    st.session_state[SS_MESSAGES] = []
    messages = st.session_state[SS_MESSAGES]

    _systemrole_content = getValueByFormnameAndKeyName("chat", "systemrole", selected_programing_model)
    messages.append({"role": "system", "content": _systemrole_content["system_role"]})

    _content = createPromt(
        _systemrole_content["prerequisites"],
        st.session_state[SS_USER_INPUT],
        _systemrole_content["srcdire"],
        _systemrole_content["ignorelist"]
    )
    user_message = {"role": "user", "content": _content}
    messages.append(user_message)

    response = client.chat.completions.create(
        model=_selected_model,
        messages=messages
    )

    bot_message = {
        "content": response.choices[0].message.content,
        "role": response.choices[0].message.role
    }

    messages.append(bot_message)

    return messages


def session_control(_selected_model, selected_programing_model):
    print("-- 21 --")
    request_messages = communicate(_selected_model, selected_programing_model)

    upsertValByKey(_selected_model, st.session_state["user_input"], request_messages)
    st.session_state["user_input"] = ""  # 入力欄を消去
    return


def init_session():
    if SS_USER_INPUT not in st.session_state:
        st.session_state[SS_USER_INPUT] = ""

    if SS_MESSAGES not in st.session_state:
        st.session_state[SS_MESSAGES] = []


def buildChatMessageFromSession():
    messages = st.session_state[SS_MESSAGES]

    for message in messages[1:]:  # 直近のメッセージを上に
        speaker = "<you>🙂"
        if message["role"] == "assistant":
            speaker = "<Agent>🤖"
            st.write(speaker + ": content")
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            with st.expander(speaker + ": content"):
                st.markdown(message["content"], unsafe_allow_html=True)


def getModelList():
    return tuple(getValueByFormnameAndKeyName("chat", "gpt", "gpt_model"))


def getProgramingLanguage():
    return tuple(getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語"))


def mainui(_title):
    col1, col2 = st.columns(2)

    init_session()

    with col1:
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

        st.button(
            "Submit",
            on_click=session_control,
            args=(
                selected_model,
                selected_programing_model,)
            )

    with col2:
        buildChatMessageFromSession()


def delete_history(subset_df, selected_index):
    _gptmodel = subset_df["gptmodel"][selected_index]
    _input = subset_df["input"][selected_index]
    _registration_date = subset_df["registration_date"][selected_index]
    deleteByKey(_gptmodel, _input, _registration_date)


def historyArea():
    col1, col2 = st.columns(2)
    with col1:
        df = pd.DataFrame(getAllHistory())
        if len(df) > 0:
            selected_index = st.number_input('Enter row index to plot:', min_value=0, max_value=len(df)-1, value=0, step=1)

            st.dataframe(df)

    with col2:
        # 選択された行のデータを取得
        if len(df) > 0:
            if 0 <= selected_index < len(df):
                subset_df = df.iloc[[selected_index]]
                messages = getValByKey(subset_df["gptmodel"][selected_index], subset_df["input"][selected_index])

                # 初期ステートの設定
                if 'show_choices' not in st.session_state:
                    st.session_state.show_choices = False
                if 'confirmed' not in st.session_state:
                    st.session_state.confirmed = False

                # アクションボタン
                if st.button('Delete History Recrod'):
                    st.session_state.show_choices = True
                    st.session_state.confirmed = False  # ユーザーが再度アクションを開始したら、確認状態をリセット

                # Yes/No の選択と確認ボタンの表示
                if st.session_state.show_choices and not st.session_state.confirmed:
                    choice = st.radio("Do you want to continue?", ('Yes', 'No'))
                    if st.button('Confirm'):
                        st.session_state.confirmed = True
                        if choice == 'Yes':
                            delete_history(subset_df, selected_index)
                            st.session_state.message = "deleted."
                        else:
                            st.session_state.message = "You chose not to continue."
                        st.session_state.show_choices = False  # 選択ウィジェットを隠す

                # 結果の表示
                if st.session_state.confirmed:
                    st.write(st.session_state.message)

                st.write(subset_df["gptmodel"][selected_index])
                st.write(subset_df["registration_date"][selected_index])
                st.write(subset_df["input"][selected_index])
                for message in messages[1:]:  # 直近のメッセージを上に
                    speaker = "<you>🙂"
                    if message["role"] == "assistant":
                        speaker = "<Agent>🤖"
                        st.write(speaker + ": content")
                        st.markdown(message["content"], unsafe_allow_html=True)
                    else:
                        with st.expander(speaker + ": content"):
                            st.markdown(message["content"], unsafe_allow_html=True)


def chat(_title):
    st.set_page_config(layout="wide")
    tab1, tab2 = st.tabs(["chat", "history"])

    with tab1:
        mainui(_title)

    with tab2:
        historyArea()
