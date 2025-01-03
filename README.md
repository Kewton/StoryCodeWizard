# StoryCodeWizard

StoryCodeWizardは、ストーリーベースの要件記述から最高のコード生成を支援するツールです。現在のプロジェクトはFastAPIやNext.jsを使用して開発されているシステム向けのコードテンプレート生成や改善案を提供します。

## 特徴
- **複数プロジェクトサポート**: プロジェクトごとに履歴を管理し、特定のプロジェクトに絞ったコード生成を行います。
- **選択可能なLLM（大規模言語モデル）**:
  - OpenAI GPTシリーズ
  - Claude (Anthropic)
  - Gemini
- **コード履歴管理**: 過去に生成したコードやプロンプトをいつでも参照履歴からダウンロード可能。
- **カスタムディレクトリと設定管理**: 各プロジェクトは異なるディレクトリ構造に対応可能。

## インストール方法

### 1. ソースコードの取得
Gitリポジトリをクローンします。
```bash
git clone https://github.com/your-repository/storycodewizard.git
cd storycodewizard
```

### 2. Python環境のセットアップ
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 機密情報の設定
以下の内容で`secret_keys.py`を作成します。
```python
openai_api_key = "<Your OpenAI API Key>"
claude_api_key = "<Your Claude API Key>"
gemini_api_key = "<Your Gemini API Key>"
```

### 4. データベースの初期化
```bash
python initdatabase.py
```

### 5. アプリケーションの起動
以下のコマンドでStreamlitアプリケーションを起動します:
```bash
streamlit run run.py
```

## 使用例
1. 初回起動後、プロジェクトの新規作成を行います。
2. 要件やソースコードを入力し、ボタン操作で各モデルによるコード生成を行います。
3. 履歴タブから過去に生成したコードやプロンプトの履歴をダウンロードすることができます。

## ディレクトリ構成

以下はこのリポジトリのディレクトリ構成です。

```
StoryCodeWizard/
├── app/
│   ├── api/                # 未使用(現在のバージョンではエンドポイント用)
│   ├── chat.py             # StreamlitフロントエンドとLLM連携ロジック
│   ├── core/               # 設定や認証ロジック予定のディレクトリ（未使用）
│   ├── models/             # データモデル予定のディレクトリ（未使用）
│   ├── schemas/            # リクエスト/レスポンス定義予定のディレクトリ
│   ├── services/           # ビジネスロジックを将来的に配置可能
│   ├── db/                 # データベースハンドリング（未使用）
│   ├── utils/              # ツールセット群
│   ├── main.py             # エントリーポイント
│   └── __init__.py
├── docs/                   # ドキュメント等
├── tests/                  # テストコード
├── requirements.txt        # 必要ライブラリ一覧
├── initdatabase.py         # 初期データ設定用スクリプト
├── run.py                  # アプリケーション起動スクリプト
├── secret_keys.py          # 各種認証情報 (gitignore済)
├── .gitignore              # 無視ファイル定義
└── README.md               # このドキュメント
```

## ドキュメントの参照

アプリケーションのAPIや仕様についての詳細な説明は MkDocs で確認可能です。

1. **必要なツールのインストール**
   ```bash
   pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python mkdocs-toc-md
   ```

2. **ローカルサーバーでドキュメントを表示**
   ```bash
   mkdocs serve
   ```

   デフォルトで `http://localhost:8000` で閲覧可能です。

## 必要環境
- Python: >= 3.9
- 推奨環境: macOS (例: MacBook Air M3)

## コントリビュート
OSSとしての貢献を歓迎します。このリポジトリは、以下の方法で貢献を募集しています。

1. プルリクエストを作成
2. Issueの登録
3. ドキュメント改善提案の提供

詳しくは[CONTRIBUTING.md](CONTRIBUTING.md)をご参照ください。

## ライセンス
このプロジェクトはMITライセンスで保護されています。