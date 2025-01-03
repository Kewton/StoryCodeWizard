from app.myjsondb.myStreamlit import upsertValueByFormnameAndKeyName


def initdata():
    upsertValueByFormnameAndKeyName(
        "chat",
        "gpt",
        {
            "gpt_model": [
                "chatgpt-4o-latest",
                "gpt-4o-mini",
                "o1-mini",
                "o1-preview",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-2.0-flash-exp",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
        }
    )

    upsertValueByFormnameAndKeyName(
        "chat",
        "systemrole",
        {
            "プログラミング言語": ["FastAPI", "Streamlit", "Next.js_1", "Next.js_2"],
            "Next.js_1": {
                "srcdire": "src",
                "libraryFileList": [
                    "package.json"
                ],
                "prerequisites": "ディレクトリにてNext.jsのフロントエンドを開発しています。利用者に最高のチャット体験を提供します。",
                "system_role": "あなたは優秀なNext.jsのフロントエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    ".DS_Store"
                ],
                "prompt": "nextjstemplate1"
            },
            "Next.js_2": {
                "srcdire": "src",
                "libraryFileList": [
                    "package.json"
                ],
                "prerequisites": "ディレクトリにてNext.jsのフロントエンドを開発しています。利用者に最高のユーザー体験を提供します。",
                "system_role": "あなたは優秀なNext.jsのフロントエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    ".DS_Store"
                ],
                "prompt": "nextjstemplate2"
            },
            "FastAPI": {
                "libraryFileList": [
                    "requirements.txt"
                ],
                "prerequisites": "./docs/requiredSpecifications.md に記載された要求仕様書に従ったFastAPIのバックエンドエンドAPIを開発しています。利用者に最高のユーザー体験を提供します。",
                "system_role": "あなたは優秀なFastAPIのバックエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    "__pycache__/",
                    "venv/",
                    ".venv/",
                    "*.db",
                    "*.DS_Store",
                    "*.log",
                    ".git/",
                    "mydb/"
                ],
                "prompt": "fastAPItemplate"
            },
            "Streamlit": {
                "srcdire": "",
                "libraryFileList": [],
                "prerequisites": "Streamlit を利用したアプリケーションのコードを生成します。利便性と可読性を確保します。",
                "system_role": "あなたは優秀なStreamlit開発者です。入力情報を元に、簡潔でメンテナブルなコードを提供してください。",
                "ignorelist": [
                    "__pycache__/",
                    "venv/",
                    ".venv/",
                    "*.db",
                    "*.DS_Store",
                    "*.log",
                    ".git/",
                    "mydb/"
                ],
                "prompt": "streamlitTemplate"  # 新しいテンプレート名
            }
        }
    )


if __name__ == '__main__':
    initdata()
