# Overview

- ブロックチェーン API サーバを実装する

# install
- pip install --user fastapi
- pip install --user uvicorn
- pip install --user ecdsa
- pip install --user requests

# Usage

## ローカル環境

- 以下のコマンドをポート番号を変えて実行する

```bash
$ CURRENT_URL="http://127.0.0.1:8001" uvicorn main:app --reload --port 8001
INFO:     Will watch for changes in these directories: ['/home/bravog/code/python/blockchain/blockchain']
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [12182] using statreload
INFO:     Started server process [12184]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

```

```bash
$ CURRENT_URL="http://127.0.0.1:8002" uvicorn main:app --reload --port 8002
```

```bash
$ CURRENT_URL="http://127.0.0.1:8003" uvicorn main:app --reload --port 8003
```

- 停止する場合は、Ctrl ＋ C を押下する

## 本番環境（インターネット環境）

<未稿>

# URL

| パス                    | 種類 | 内容                               |
| ----------------------- | ---- | ---------------------------------- |
| /get_transaction_pool   | GET  | トランザクションプール参照         |
| /put_transaction        | POST | トランザクションデータ登録／同報   |
| /recieve_transaction    | POST | トランザクションデータ同報更新     |
| /get_chain              | GET  | ブロックチェーン参照               |
| /create_block/{creator} | POST | ブロック生成・ブロックチェーン同報 |
| /recieve_chain          | POST | ブロックチェーン同報更新           |
