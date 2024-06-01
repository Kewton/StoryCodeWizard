from app.myjsondb.myStreamlit import upsertValueByFormnameAndKeyName


def initdata():
    upsertValueByFormnameAndKeyName(
        "chat",
        "gpt",
        {
            "gpt_model": [
                "gpt-4o",
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-4-32k",
                "gpt-4-turbo",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
        }
    )

    upsertValueByFormnameAndKeyName(
        "chat",
        "systemrole",
        {
            "プログラミング言語": ["Next.js_1", "Next.js_2"],
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
            }
        }
    )


if __name__ == '__main__':
    initdata()
