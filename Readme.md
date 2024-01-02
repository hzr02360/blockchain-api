# ブロックチェーン API サーバ

- python3 でブロックチェーン API サーバを実装する

## 環境

- python3 と以下のフレームワーク・ライブラリ

| ライブラリ名                                             | 用途                                |
| -------------------------------------------------------- | ----------------------------------- |
| [FastAPI](https://fastapi.tiangolo.com/ja/)              | API 実装用の Web フレームワーク     |
| [Uvicorn](https://www.uvicorn.org/)                      | Python 用の ASGI ウェブサーバー実装 |
| [ecdsa](https://pypi.org/project/ecdsa/)                 | 暗号アルゴリズムライブラリ          |
| [requests](https://pypi.org/project/requests/)           | Python で使われる HTTP ライブラリ   |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 環境変数を扱うためのライブラリ      |
| [pyyaml](https://pypi.org/project/PyYAML/)               | yaml ファイルを扱うためのライブラリ |

- Ubuntu 22.04.3 LTS
- [Render](https://render.com/)

## 実行方法

### ローカル環境

- `.env`ファイルにローカル環境のサーバ URL を定義する

```bash
URL_TO_LINK="
http://127.0.0.1:8001,
http://127.0.0.1:8002,
http://127.0.0.1:8003
"
```

- 以下のコマンドをポート番号を変えて実行する

```bash
$ uvicorn blockchain.controller:app --reload --port 8001
INFO:     Will watch for changes in these directories: ['/~略~/blockchain-api']
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [142089] using StatReload
2024-01-01 18:01:53,651 uvicorn.error:76 serve [INFO]: Started server process [142091]
2024-01-01 18:01:53,651 uvicorn.error:46 startup [INFO]: Waiting for application startup.
2024-01-01 18:01:53,651 uvicorn.error:60 startup [INFO]: Application startup complete.
```

```bash
$ uvicorn blockchain.controller:app --reload --port 8002
```

```bash
$ uvicorn blockchain.controller:app --reload --port 8003
```

- 停止する場合は、Ctrl ＋ C を押下する

### 公開環境（インターネット環境）

- [Render](https://render.com/) を利用する
- GitHub にソースコードをアップロードする
- Render と GitHub を連携する
- 以下の手順で Render に `Web Service` を生成しデプロイする
  - Name: 任意の名前（サーバ名として使用する）
  - Region: 近そうな任意の値
  - Instance Type: Free
  - Repository: GitHub リポジトリの URL
  - Branch: GitHub リポジトリのブランチ名
  - Build Command: pip install -r requirements.txt
  - Start Command: uvicorn blockchain.controller:app --host 0.0.0.0 --port 10000
- デプロイしたサーバの環境変数`.env`に通信先のサーバ URL を設定する

### アクセス可能な URL

| パス                   | 種類 | 内容                                                                                       |
| ---------------------- | ---- | ------------------------------------------------------------------------------------------ |
| get_transaction_pool   | GET  | トランザクションプールを参照する                                                           |
| put_transaction        | POST | トランザクションデータを登録し他サーバに配信する                                           |
| recieve_transaction    | POST | 配信されたトランザクションデータで自サーバのデータを更新する                               |
| get_chain              | GET  | ブロックチェーンを参照する                                                                 |
| create_block/{creator} | POST | ブロックを生成しブロックチェーンを配信する<br>creater にはブロック生成者の公開鍵を設定する |
| recieve_chain          | POST | 配信されたブロックチェーンで自サーバのチェーンを更新する                                   |

## 実装

### フォルダとファイル構成

```
../blockchain-api/
├── Readme.md
├── blockchain
│   ├── __pycache__
│   ├── blockchain.py
│   ├── common
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── const.py
│   │   ├── credential.py
│   │   └── logger.py
│   ├── controller.py
│   └── model.py
├── logger.yml
└── requirements.txt
```

### ソースコード一覧

| ファイル名             | 用途 　                                                                      |
| ---------------------- | ---------------------------------------------------------------------------- |
| `controller.py`        | URL を定義し `blockchain.py`の各処理を呼び出す                               |
| `blockchain.py`        | ブロックチェーン API の各処理を実装する                                      |
| `model.py`             | 以下のデータ型を定義する<br>トランザクション<br>ブロック<br>ブロックチェーン |
| `common.const.py`      | 定数定義                                                                     |
| `common.credential.py` | 公開鍵やシグネチャに関連する処理を実装する                                   |
| `common.logger.py`     | ロガーを実装する                                                             |

### 設定ファイル

| ファイル名         | 用途 　                                              |
| ------------------ | ---------------------------------------------------- |
| `requirements.txt` | API サーバデプロイ時に必要な追加ライブラリを定義する |
| `logger.yml`       | ロガーに関する定義ファイル                           |
