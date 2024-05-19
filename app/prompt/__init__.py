from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents


def createPromt(_systemrole_content, _input):
    _prerequisites = _systemrole_content["prerequisites"]
    _libraryFileList = _systemrole_content["libraryFileList"]
    _src_root_path = _systemrole_content["srcdire"]
    _ignorelist = _systemrole_content["ignorelist"]

    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。

### 前提条件
{_prerequisites}

### 制約条件
- アウトプットはmarkdown形式とすること
- 要求文書を適切な表現に変換すること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- 新規にインストールが必要な場合、ライブラリのインストール方法を明確にすること
- 新規にファイル作成が必要な場合、名称と拡張子も明確にしソースコードをフルで出力すること
- git への commit コメントを出力すること

### 要求
{_input}

### 現在のpackage.json
{fetch_libraryfiles_and_contents(_libraryFileList)}

### 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
    return _content
