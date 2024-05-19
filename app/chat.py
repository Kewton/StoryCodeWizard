import streamlit as st
import pandas as pd
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName
from app.myjsondb.myHistory import getValByKey, upsertValByKey, getAllHistory, deleteByKey
from app.prompt import createPromt
from app.util.execLlmApi import execLlmApi
import base64


# sesson state key
SS_USER_INPUT = "user_input"
SS_MESSAGES = "messages"


# チャットボットとやりとりする関数
def communicate(_selected_model, selected_programing_model, encoded_file):
    st.session_state[SS_MESSAGES] = []
    messages = st.session_state[SS_MESSAGES]

    _systemrole_content = getValueByFormnameAndKeyName("chat", "systemrole", selected_programing_model)
    messages.append({"role": "system", "content": _systemrole_content["system_role"]})

    _content = createPromt(
        _systemrole_content,
        st.session_state[SS_USER_INPUT]
    )
    user_message = {"role": "user", "content": _content}
    messages.append(user_message)

    message_content, message_role = execLlmApi(_selected_model, messages, encoded_file)

    bot_message = {
        "content": message_content,
        "role": message_role
    }

    messages.append(bot_message)

    return messages


def story2code(_selected_model, selected_programing_model, encoded_file):
    request_messages = communicate(_selected_model, selected_programing_model ,encoded_file)

    upsertValByKey(_selected_model, st.session_state["user_input"], request_messages)
    st.session_state["user_input"] = ""  # 入力欄を消去
    return


def init_session():
    if SS_USER_INPUT not in st.session_state:
        st.session_state[SS_USER_INPUT] = ""

    if SS_MESSAGES not in st.session_state:
        st.session_state[SS_MESSAGES] = []


def buildChatMessageFromSession(messages):

    for message in messages[1:]:  # 直近のメッセージを上に
        speaker = "<you>🙂"
        if message["role"] == "assistant":
            speaker = "<Agent>🤖"
            st.write(speaker + ": content")
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            with st.expander(speaker + ": content"):
                st.markdown(message["content"], unsafe_allow_html=True)

            with open("./output.txt", "w") as file:
                file.write(message["content"])


def getModelList():
    return tuple(getValueByFormnameAndKeyName("chat", "gpt", "gpt_model"))


def getProgramingLanguage():
    return tuple(getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語"))


def mainui():
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
            "ユーザーストーリを入力してください。",
            key="user_input",
            value=st.session_state[SS_USER_INPUT])

        # ファイルアップロード
        uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=['jpeg'])
        encoded_file = ""

        if uploaded_file is not None:
            # ファイルの内容を読み込み
            file_contents = uploaded_file.read()
            
            # base64エンコード
            encoded_file = base64.b64encode(file_contents).decode('utf-8')

        st.button(
            "実行",
            on_click=story2code,
            args=(
                selected_model,
                selected_programing_model,
                encoded_file,)
            )

    with col2:
        messages = st.session_state[SS_MESSAGES]
        buildChatMessageFromSession(messages)


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
                messages = getValByKey(df["gptmodel"][selected_index], df["input"][selected_index])

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
                            delete_history(df, selected_index)
                            st.session_state.message = "deleted."
                        else:
                            st.session_state.message = "You chose not to continue."
                        st.session_state.show_choices = False  # 選択ウィジェットを隠す

                # 結果の表示
                if st.session_state.confirmed:
                    st.write(st.session_state.message)

                st.write(df["gptmodel"][selected_index])
                st.write(df["registration_date"][selected_index])
                st.write(df["input"][selected_index])

                buildChatMessageFromSession(messages)


def chat():
    st.set_page_config(layout="wide")
    st.title("StoryCodeWizard")
    tab1, tab2 = st.tabs(["stroy2code", "history"])

    with tab1:
        mainui()

    with tab2:
        historyArea()
