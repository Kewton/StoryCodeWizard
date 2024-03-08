from localjsondb.jsonDB import ValidatedSchemaFactory, BaseJsonDbORM, DoFactory


class _MyStreamlitProp:
    formname: str
    keyname: str
    value: dict

class _MyStreamlitSchema(_MyStreamlitProp, ValidatedSchemaFactory):
    pass

class MyStreamlitDo(_MyStreamlitProp, DoFactory):
    pass

class MyStreamlitOrm(BaseJsonDbORM):
    dbpath = "./mydb/system"
    schema = _MyStreamlitSchema 

    def __init__(self, _dbname):
        self.dbname = _dbname
        super().__init__()
    
MyStremalit = MyStreamlitOrm("myStreamlit")