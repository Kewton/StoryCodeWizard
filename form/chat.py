import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
from secret_keys import openai_api_key

load_dotenv()

client = OpenAI(
  api_key=openai_api_key
)

# チャットボットとやりとりする関数
def communicate(_selected_response_format):
    messages = st.session_state["messages"]

    if "normal" == _selected_response_format:
        user_message = {"role": "user", "content": st.session_state["user_input"]}
        messages.append(user_message)
        response = client.chat.completions.create(
            model="gpt-4", # gpt-3.5-turbo
            messages=messages
        )
    else:
        messages.append({"role": "system", "content": "あなたは返答をすべてJSON形式で出力します。"})
        messages.append({"role": "user", "content": st.session_state["user_input"]})
        response = client.chat.completions.create(
            model="gpt-4", # gpt-3.5-turbo
            response_format={"type":_selected_response_format},
            messages=messages
        )

    bot_message = {
        "content": response.choices[0].message.content,
        "role": response.choices[0].message.role
    }
        
    messages.append(bot_message)

def session_control(_selected_response_format):
    
    communicate(_selected_response_format)
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

    selected_response_format = st.selectbox("Choose Response format", ("normal", "json_object"))
    user_input = st.text_area("メッセージを入力してください。", key="user_input", value=st.session_state["user_input"])
    submit_button = st.button("Submit", on_click=session_control,args=(selected_response_format,))