from localjsondb.jsonDB import ValidatedSchemaFactory, BaseJsonDbORM, DoFactory


class _RagDocProp:
    dataset_name: str
    dataset_description: str = ""
    markdown_text: str = ""

class _RagDocSchema(_RagDocProp, ValidatedSchemaFactory):
    pass

class RagDocDo(_RagDocProp, DoFactory):
    pass

class RagDocOrm(BaseJsonDbORM):
    schema = _RagDocSchema 

    def __init__(self, _dbdir, _dbname):
        self.dbpath = f"./mydb/{_dbdir}"
        self.dbname = _dbname
        super().__init__()
    
ragDB = RagDocOrm("v0.0.1", "rag")