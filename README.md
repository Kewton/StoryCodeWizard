create secret_keys.py
```python
openai_api_key = <your api key>
claude_api_key = <your api key>
gemini_api_key = <your api key>
```

# initialize
```
python3 initdatabase.py
```

# setup(macbook)
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# memo
- 最新のソースとユーザーストーリーをインプットするとコードが出力される
- input
    - コード
        - package.json
        - jsx
    - ユースケース

# run
```
# 設定ファイル初期化
python initdatabase.py

# 起動
streamlit run run.py
```

# 参考

## Next.js
Next.jsは下記コマンドによるプロジェクト作成を前提とする
```
npx create-next-app@latest myux \
  --app \
  --ts \
  --tailwind \
  --eslint \
  --src-dir
```

python generate_files.py ./chat_history_claude-sonnet-4-20250514_2025-05-30_23_52_20_agent.md -d /Users/maeno.kota/work/git/storycodewizardnext