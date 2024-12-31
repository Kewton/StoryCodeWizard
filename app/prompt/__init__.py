from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents


def createPromt(_systemrole_content, _input):
    _prerequisites = _systemrole_content["pjdir"] + _systemrole_content["prerequisites"]

    # _libraryFileList = _systemrole_content["libraryFileList"]
    _libraryFileList = []
    for a in _systemrole_content["libraryFileList"]:
        _libraryFileList.append(_systemrole_content["pjdir"] + "/" + a)
    _src_root_path = _systemrole_content["pjdir"] + "/" + _systemrole_content["srcdire"]
    _ignorelist = _systemrole_content["ignorelist"]

    # print("_systemrole_content")
    # print(_systemrole_content["prompt"])

    if "nextjstemplate1" == _systemrole_content["prompt"]:
        return nextjstemplate1(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    elif "nextjstemplate2" == _systemrole_content["prompt"]:
        return nextjstemplate2(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    elif "fastAPItemplate" == _systemrole_content["prompt"]:
        return fastAPItemplate(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    else:
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


def nextjstemplate1(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist):
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


def nextjstemplate2(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。
- 必要に応じて改善案を提案して下さい。

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


def fastAPItemplate(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し、下記手順に従って前提条件と制約条件と技術制約を満たす最高の成果物を生成してください。
    1. 要求を解釈し推敲を行う。また、必要に応じて情報を補完する。
    2. ソースコードが存在する場合、現状を把握する。
    3. 出力結果への評価方法及び前提条件と制約条件と技術制約を満たした合格条件を定義する。
    4. 合格条件に合うコードもしくはテキストを出力する
    5. 3の評価方法に従って評価する
    6. 評価結果が合格の場合終了する。不合格の場合は7に進む。
    7. 不合格の原因を調査し解決策を検討する
    8. 2からやり直す

# 前提条件
- {_prerequisites}
- 開発環境は「macbook air m3」です

# 制約条件
- 出力結果はmarkdown形式とすること
- ソースコードはGoogleスタイル形式でのPython Docstringも出力すること
- pytestによるテストコードとテストの実行方法を出力すること
- README.mdへの記述内容も出力すること
- ソースコードとテキスト共に途中を省略せずに全てを出力すること
- 新規にライブラリのインストールが必要な場合、ライブラリのインストール方法を明確にすること
- 新規にファイル作成が必要な場合、ファイル名と拡張子を明確にしソースコードをフルで出力すること
- 修正が必要な場合は、類似の修正であっても全ての対象箇所を出力すること
- 修正時は、修正後の全てのコードに加えdiff形式で変更箇所が明らかになるように出力すること
- ./docs/requiredSpecifications.md（要求仕様書）の変更が発生する場合は修正内容を出力すること
- git への commit コメントを出力すること
- 出力結果の妥当性の評価方法及び評価結果を出力すること
- 出力結果に問題が残る場合は再度検討しブラッシュアップすること

# 技術制約
- databaseはSQLiteを使用すること
- ディレクトリ構成は下記例に準拠こと
    ```
    <myproject>/
    ├── app/
    │   ├── api/                # エンドポイント（ルーター）のディレクトリ
    │   │   ├── v1/
    │   │   │   ├── endpoints/  # 個別のエンドポイントファイル
    │   │   │   │   ├── user.py # 例: ユーザー関連のエンドポイント
    │   │   │   │   ├── item.py # 例: アイテム関連のエンドポイント
    │   │   │   └── __init__.py
    │   ├── core/               # 設定や重要なロジック（例: 認証設定）
    │   │   ├── config.py       # 設定ファイル
    │   │   ├── security.py     # セキュリティ関連の設定や認証処理
    │   │   └── __init__.py
    │   ├── models/             # データベースモデル（SQLAlchemyなど）
    │   │   ├── user.py         # 例: ユーザーモデル
    │   │   ├── item.py         # 例: アイテムモデル
    │   │   └── __init__.py
    │   ├── schemas/            # データバリデーションやリクエスト/レスポンスのスキーマ
    │   │   ├── user.py         # 例: ユーザー関連のスキーマ
    │   │   ├── item.py         # 例: アイテム関連のスキーマ
    │   │   └── __init__.py
    │   ├── services/           # ビジネスロジック（アプリケーションのサービス層）
    │   │   ├── user_service.py # 例: ユーザー関連のビジネスロジック
    │   │   ├── item_service.py # 例: アイテム関連のビジネスロジック
    │   │   └── __init__.py
    │   ├── db/                 # データベース接続や設定
    │   │   ├── base.py         # モデルのベース設定
    │   │   ├── session.py      # DBセッションの設定
    │   │   └── __init__.py
    │   ├── utils/              # ヘルパー関数やユーティリティ関数
    │   │   ├── helpers.py
    │   │   └── __init__.py
    │   ├── main.py             # アプリケーションのエントリーポイント
    │   └── __init__.py
    ├── .env                    # 環境変数ファイル
    ├── tests                   # pytestによるテストコード
    │   ├── test_user.py        # 例: ユーザー関連のテスト
    │   └── test_item.py        # 例: アイテム関連のテスト
    ├── docs                    # mkdocsによるドキュメント
    │   ├── index.md            # mkddocsのhome画面
    │   ├── reference.md        # appディレクトリのコードから自動生成下ドキュメント
    │   └── requiredSpecifications.md # 要求仕様書
    ├── requirements.txt        # Pythonの依存パッケージ
    └── Dockerfile              # Dockerの設定ファイル（必要に応じて）
    ```

---
# 要求
    {_input}

---
# 現在のrequirements.txt
{fetch_libraryfiles_and_contents(_libraryFileList)}

---
# 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
    return _content