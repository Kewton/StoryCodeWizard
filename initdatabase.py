from app.myjsondb.myStreamlit import upsertValueByFormnameAndKeyName


def initdata():
    upsertValueByFormnameAndKeyName(
        "chat",
        "gpt",
        {
            "gpt_model": [
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-4-32k",
                "gpt-4-turbo"
            ]
        }
    )

    upsertValueByFormnameAndKeyName(
        "chat",
        "systemrole",
        {
            "プログラミング言語": ["Next.js"],
            "Next.js": {
                "srcdire": "./front/src",
                "prerequisites": "'./front'ディレクトリにてNext.jsのフロントエンドを開発しています",
                "system_role": "あなたは優秀なNext.jsのフロントエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    ".DS_Store"
                ]
            }
        }
    )


if __name__ == '__main__':
    initdata()
