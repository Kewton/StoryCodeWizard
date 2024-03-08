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

    MyStremalit.upsert(myStreamlitDo)