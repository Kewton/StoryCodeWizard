from myjsondb.myStreamlit import MyStreamlitDo, MyStremalit


if __name__ == '__main__':
    myStreamlitDo = MyStreamlitDo()
    myStreamlitDo.formname = "main"
    myStreamlitDo.keyname = "form_menu"
    myStreamlitDo.value = {
        "form_menu":[
            "チャット",
            "ドキュメント登録",
            "ドキュメント編集"
        ]
    }

    MyStremalit.upsertByprimaryKey(myStreamlitDo)

    myStreamlitDo_chat = MyStreamlitDo()
    myStreamlitDo_chat.formname = "chat"
    myStreamlitDo_chat.keyname = "gpt"
    myStreamlitDo_chat.value = {
        "gpt_model":[
            "gpt-4",
            "gpt-4-32k",
            "gpt-4-turbo"
        ]
    }

    MyStremalit.upsertByprimaryKey(myStreamlitDo_chat)

    myStreamlitDo_systemrole = MyStreamlitDo()
    myStreamlitDo_systemrole.formname = "chat"
    myStreamlitDo_systemrole.keyname = "systemrole"
    myStreamlitDo_systemrole.value = {
        "プログラミング言語":["Next.js"],
        "Next.js": ["あなたは優秀なNext.jsのフロントエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。"]
    }

    MyStremalit.upsertByprimaryKey(myStreamlitDo_systemrole)