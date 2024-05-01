from localjsondb.jsonDB import ValidatedSchemaFactory, BaseJsonDbORM, DoFactory


class _MyHistoryProp:
    gptmodel: str
    input: str
    contentList: list = []


class _MyHistorySchema(_MyHistoryProp, ValidatedSchemaFactory):
    pass


class MyHistoryDo(_MyHistoryProp, DoFactory):
    pass


class MyHistoryOrm(BaseJsonDbORM):
    dbpath = "./mydb/tran"
    schema = _MyHistorySchema

    def __init__(self, _dbname):
        self.dbname = _dbname
        super().__init__()


MyHistory = MyHistoryOrm("myHistory")


def getValByKey(gptmodel, input):
    myHistoryDo = MyHistoryDo()
    myHistoryDo.gptmodel = gptmodel
    myHistoryDo.input = input
    for a in MyHistory.jsondb.getByQuery(myHistoryDo.to_query_dict()):
        return a["contentList"]

    return []


def getAllHistory():
    out = []
    for a in MyHistory.jsondb.getAll():
        out.append({
            "gptmodel": a["gptmodel"],
            "input": a["input"],
            "registration_date": a["registration_date"]
        }
        )

    return out


def upsertValByKey(_gptmodel, input, contentList):
    myHistoryDo_systemrole = MyHistoryDo()
    myHistoryDo_systemrole.gptmodel = _gptmodel
    myHistoryDo_systemrole.input = input
    myHistoryDo_systemrole.contentList = contentList

    MyHistory.upsertByprimaryKey(myHistoryDo_systemrole)


def deleteByKey(_gptmodel, _input, _registration_date):
    myHistoryDo_systemrole = MyHistoryDo()
    myHistoryDo_systemrole.gptmodel = _gptmodel
    myHistoryDo_systemrole.input = _input
    myHistoryDo_systemrole.registration_date = _registration_date
    MyHistory.delete(myHistoryDo_systemrole)
