from openai import OpenAI
from secret_keys import openai_api_key, claude_api_key
import anthropic


chatgptapi_client = OpenAI(
  api_key=openai_api_key
)

claude_client = anthropic.Anthropic(
    api_key=claude_api_key,
)


def execLlmApi(_selected_model, _messages, encoded_file):
    if "gpt" in _selected_model:
        if "gpt-4o" == _selected_model and len(encoded_file) > 0:
            _inpurt_messages = []
            _inpurt_messages.append(_messages[0])
            _inpurt_messages.append(
                {"role": "user", "content": [
                    {"type": "text", "text": _messages[1]["content"]},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_file}"}}
                ]}
            )
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model,
                messages=_inpurt_messages
            )
        else:
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model,
                messages=_messages
            )
        print("_messages = ")
        print(_messages)
        return response.choices[0].message.content, response.choices[0].message.role

    elif "claude" in _selected_model:
        _inpurt_messages = []

        for _rec in _messages:
            if _rec["role"] == "system":
                _systemrole = _rec["content"]
            elif _rec["role"] == "user":
                if len(encoded_file) > 0:
                    print("append image")
                    _content = []
                    _content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_file
                        }
                    })
                    _content.append({
                        "type": "text",
                        "text": _rec["content"]
                    })
                    
                    _inpurt_messages.append(
                        {
                            "role": _rec["role"],
                            "content": _content
                        }
                    )
                else:
                    _inpurt_messages.append(_rec)

        response = claude_client.messages.create(
            max_tokens=4096,
            system=_systemrole,
            model=_selected_model,
            messages=_inpurt_messages
        )

        return response.content[0].text, response.role
    else:
        return {}, ""
