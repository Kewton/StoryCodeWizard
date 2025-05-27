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
python initdatabase.py
streamlit run run.py
```

```
npx create-next-app@latest myux \
  --app \
  --ts \
  --tailwind \
  --eslint \
  --src-dir
```

```
python generate_files.py ./myproject/history/chat_history_claude-sonnet-4-20250514_2025-05-27_09_34_55_agent.md -d ./myproject/myux
```

<変更後のREADME.md *README.mdのみ全体をインデントしたものを出力すること。また、README.md内のコードブロックはコードブロック全体をさらにインデントすること。>