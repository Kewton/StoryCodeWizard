from openai import OpenAI
from secret_keys import openai_api_key


chatgptapi_client = OpenAI(
  api_key=openai_api_key
)


def execLlmApi(_selected_model, _messages):
    response = chatgptapi_client.chat.completions.create(
        model=_selected_model,
        messages=_messages
    )
    return response

