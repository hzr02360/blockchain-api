# Overview

- ブロックチェーン API サーバを実装する

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

- 停止する場合は、Ctrl ＋ C を押下する

## 本番環境（インターネット環境）
