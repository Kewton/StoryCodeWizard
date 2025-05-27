import streamlit as st
import pandas as pd
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName
from app.myjsondb.myHistories import createProject, getProjectList, dropProject, upsertValToPjByKey, getAllHistoryOfPj, getValOfPjByKey, deletePjByKey
from app.myjsondb.myProjectSettings import upsertPjdirAndValueByPjnm, getPjdirByPjnm, deletePjSettingsByKey, getAllProject
from app.prompt import createPromt
from app.util.execLlmApi import execLlmApi
import base64
import os


# sesson state key
SS_USER_INPUT = "user_input"
SS_MESSAGES = "messages"


# チャットボットとやりとりする関数
def communicate(selected_project, _selected_model, selected_programing_model, encoded_file):
    st.session_state[SS_MESSAGES] = []
    messages = st.session_state[SS_MESSAGES]

    _systemrole_content = getValueByFormnameAndKeyName("chat", "systemrole", selected_programing_model)
    _systemrole_content["pjdir"] = getPjdirByPjnm(selected_project)
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


def story2code(selected_project, _selected_model, selected_programing_model, encoded_file):
    request_messages = communicate(selected_project, _selected_model, selected_programing_model, encoded_file)

    print(f"selected_project = {selected_project}")
    upsertValToPjByKey(_selected_model, st.session_state["user_input"], request_messages, selected_project)

    st.session_state["user_input"] = ""  # 入力欄を消去
    return


def init_session():
    if SS_USER_INPUT not in st.session_state:
        st.session_state[SS_USER_INPUT] = ""

    if SS_MESSAGES not in st.session_state:
        st.session_state[SS_MESSAGES] = []


def get_download_user_str(messages):
    """Create a formatted string from messages"""
    for message in messages[1:]:
        if message["role"] == "user":
            return message['content']
    return ""


def get_download_assistant_str(messages):
    """Create a formatted string from messages"""
    for message in messages[1:]:
        if message["role"] == "assistant":
            return message['content']
    return ""


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


def getModelList():
    return tuple(getValueByFormnameAndKeyName("chat", "gpt", "gpt_model"))


def getProgramingLanguage():
    return tuple(getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語"))


def getProjectListTuple():
    return tuple(getAllProject())


def mainui():
    col1, col2 = st.columns(2)

    init_session()

    with col1:
        selected_project = st.selectbox(
            "Choose Project",
            getProjectListTuple(),
            key="selected_project")

        selected_model = st.selectbox(
            "Choose Gpt Model",
            getModelList(),
            key="selected_model")

        selected_programing_model = st.selectbox(
            "Choose Programing Language",
            getProgramingLanguage(),
            key="selected_programing_language")

        st.text_area(
            "要求を入力してください。",
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
                selected_project,
                selected_model,
                selected_programing_model,
                encoded_file,)
            )

    with col2:
        messages = st.session_state[SS_MESSAGES]
        buildChatMessageFromSession(messages)


def delete_history(subset_df, selected_index, selected_project):
    _gptmodel = subset_df["gptmodel"][selected_index]
    _input = subset_df["input"][selected_index]
    _registration_date = subset_df["registration_date"][selected_index]
    deletePjByKey(_gptmodel, _input, _registration_date, selected_project)


def historyArea():
    col1, col2 = st.columns(2)
    with col1:
        selected_project = st.selectbox(
            "Choose Project",
            getProjectListTuple(),
            key="selected_project_of_historyArea")
        data = getAllHistoryOfPj(selected_project)
        if not data or not isinstance(data, list) or len(data) == 0:
            st.write("履歴がありません。")
            return
        df = pd.DataFrame(data)
        # 必要なカラムがなければエラー回避
        required_cols = {'registration_date', 'gptmodel', 'input'}
        if not required_cols.issubset(df.columns):
            st.write("履歴データに必要なカラムがありません。")
            return
        df = df.sort_index(ascending=False)
        df = df.reset_index(drop=True)
        df['registration_date'] = (
            df['registration_date']
            .str[:14]
            .apply(lambda x: f"{x[:4]}-{x[4:6]}-{x[6:8]}_{x[8:10]}:{x[10:12]}:{x[12:14]}")
        )
        columns_order = ['registration_date', 'gptmodel', 'input']
        df = df[columns_order]
        if len(df) > 0:
            selected_index = st.number_input('Enter row index to plot:', min_value=0, max_value=len(df)-1, value=0, step=1)
            st.dataframe(df)

    with col2:
        # 選択された行のデータを取得
        if len(df) > 0:
            if 0 <= selected_index < len(df):
                messages = getValOfPjByKey(df["gptmodel"][selected_index], df["input"][selected_index], selected_project)

                # 初期ステートの設定
                if 'show_choices' not in st.session_state:
                    st.session_state.show_choices = False
                if 'confirmed' not in st.session_state:
                    st.session_state.confirmed = False

                # ボタンを横に並べるためにcolumnsを使用
                button_col1, button_col2, button_col3 = st.columns(3)

                # Delete History Recordボタン
                with button_col1:
                    if st.button('Delete History Record'):
                        st.session_state.show_choices = True
                        st.session_state.confirmed = False

                with button_col2:
                    download_str_user = get_download_user_str(messages)
                    st.download_button(
                        label="Download Your Context",
                        data=download_str_user,
                        file_name=f"chat_history_{df['gptmodel'][selected_index]}_{df['registration_date'][selected_index]}_user.md",
                        mime="text/plain"
                    )

                with button_col3:
                    download_str_assistant = get_download_assistant_str(messages)
                    st.download_button(
                        label="Download Agent Context",
                        data=download_str_assistant,
                        file_name=f"chat_history_{df['gptmodel'][selected_index]}_{df['registration_date'][selected_index]}_agent.md",
                        mime="text/plain"
                    )

                # Yes/No の選択と確認ボタンの表示
                if st.session_state.show_choices and not st.session_state.confirmed:
                    choice = st.radio("Do you want to continue?", ('Yes', 'No'))
                    if st.button('Confirm'):
                        st.session_state.confirmed = True
                        if choice == 'Yes':
                            delete_history(df, selected_index, selected_project)
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


def project():
    # プロジェクトの新規作成と一覧の確認と削除を行う方法
    # 新規プロジェクトの作成
    st.header("新規プロジェクトの作成")
    new_project_name = st.text_input("プロジェクト名")
    dir_path = st.text_input("ディレクトリのパスを入力してください:")

    if st.button("プロジェクトを追加"):
        # 入力されたディレクトリパスが有効かどうかを確認
        if dir_path:
            if os.path.isdir(dir_path):
                if new_project_name:
                    createProject(new_project_name)
                    upsertPjdirAndValueByPjnm(new_project_name, dir_path, {"test": "sss"})
                    st.success(f"プロジェクト '{new_project_name}' を追加しました。")
                    st.success(f"指定されたディレクトリ: {getPjdirByPjnm(new_project_name)}")
                else:
                    st.error("プロジェクト名を入力してください。")
            else:
                st.error("有効なディレクトリパスを入力してください。")
        else:
            st.error("ディレクトリパスを入力してください。")

    # プロジェクト一覧の表示と削除
    st.header("プロジェクト一覧")
    projects = getProjectList()
    if projects:
        for project_name in projects:
            st.write(f"- {project_name}")
            if st.button(f"削除 '{project_name}'", key=project_name):
                dropProject(project_name)
                deletePjSettingsByKey(project_name)
                st.success(f"プロジェクト '{project_name}' を削除しました。")
    else:
        st.write("現在、プロジェクトはありません。")


def chat():
    st.set_page_config(layout="wide")
    st.title("StoryCodeWizard")
    tab1, tab2, tab3 = st.tabs(["Stroy2Code", "MyHistory", "Project List"])

    with tab1:
        mainui()

    with tab2:
        historyArea()

    with tab3:
        project()
