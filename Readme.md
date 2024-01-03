# ブロックチェーン API サーバ

- python3 でブロックチェーン API サーバを実装する
- こちらから派生しています  
  https://github.com/moyattodataman/blockchain/tree/main

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
URL_TO_LINK="http://127.0.0.1:8001,http://127.0.0.1:8002,http://127.0.0.1:8003"
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
- デプロイしたサーバの環境変数に通信先のサーバ URL を設定する（自サーバ URL 以外を設定しておく）

```bash
URL_TO_LINK=https://blockchain-api-02.onrender.com,https://blockchain-api-03.onrender.com
```

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

### 取り扱うデータ

トランザクション`<Transaction>`

| 項目名         | 物理名      | 型  | 説明                                                       |
| -------------- | ----------- | --- | ---------------------------------------------------------- |
| タイムスタンプ | time        | str | トランザクション生成時のタイムスタンプ                     |
| 送金者         | sender      | str | データ送信元の公開鍵                                       |
| 受取人         | reciever    | str | データ受取先の公開鍵                                       |
| 金額           | amount      | int | 取引金額                                                   |
| 説明           | description | str | 取引内容                                                   |
| 電子署名       | signature   | str | データのシグネチャ<br>データと送信者の秘密鍵で生成した署名 |

ブロック`<Block>`

| 項目名                 | 物理名       | 型                | 説明                                                              |
| ---------------------- | ------------ | ----------------- | ----------------------------------------------------------------- |
| タイムスタンプ         | time         | str               | ブロック生成時のタイムスタンプ                                    |
| トランザクションリスト | transactions | List[Transaction] | 生成済みトランザクションのリスト                                  |
| ハッシュ値             | hash         | str               | 一つ前のブロックのハッシュ値                                      |
| ナンス                 | nonce        | int               | 「Number Of Onece」の略。ブロックが正当か否かを検証するための数値 |

ブロックチェーン`<Chain>`

| 項目名         | 物理名 | 型          | 説明                     |
| -------------- | ------ | ----------- | ------------------------ |
| ブロックリスト | blocks | List[Block] | 生成済みブロックのリスト |

## データ処理の流れ

トランザクションの生成〜登録

- API サーバを利用するクライアントは、Transaction 型のデータを生成し、API サーバに送信する
  - リクエストパスは`/put_transaction`
- API サーバは以下の処理を実行する
  - トランザクションデータが正しいか検証する
  - 自身のトランザクションプールに登録する
  - 他の API サーバにトランザクションデータを同報する
    - リクエストパスは`/recieve_transaction`
- 同報を受けとった API サーバは以下の処理を実行する
  - トランザクションデータが正しいか検証する
  - 自身のトランザクションプールに登録する
- トランザクションが発生する都度、上記処理を繰り返す

ブロック生成およびブロックチェーン更新

- マイニングと呼ばれる処理
- マイニング実行者は自分自身の公開鍵を指定して API サーバにアクセスする
  - リクエストパスは`/create_block/{creator}`
  - `{creator}` に公開鍵を指定する
- API サーバは以下の処理を実行する
  - リワードトランザクションを生成しトランザクションプールに登録する
  - 最後のブロックのハッシュ値を生成する
  - ナンスを得るためのハッシュ値計算を繰り返す
  - ブロックを生成しブロックチェーンに追加する
  - 今回生成したブロックに含むトランザクションデータをトランザクションプールから削除する
  - 他の API サーバにブロックチェーンを同報する
    - リクエストパスは`/recieve_chain`
- 同報を受けとった API サーバは以下の処理を実行する
  - 受信したブロックチェーンを検証する
  - 受信したブロックチェーンで自身のブロックチェーンを置き換える
  - 受信したブロックチェーンの最終ブロックが含んでいるトランザクションデータをトランザクションプールから削除する

> リワードトランザクションは、ブロック報酬(block reword)を割り当てるためのトランザクションを指す。
> 参考：[ブロック報酬とは？【GW に考える暗号資産の基本】](https://www.coindeskjapan.com/141478/)

##　セキュリティ

トランザクションデータの検証

- 公開鍵を使用して、以下のデータに整合性があるか検証する
  - トランザクションデータの電子署名（Byte 形式）
  - 電子署名を除いたトランザクションデータ（json 形式）

ブロックチェーンの検証

- 受信したブロックチェーンのブロック数が、自身の保持しているブロック数に満たない場合は NG とする
- 受信したブロックチェーンのブロックに対し以下を検証する
  - 先頭ブロックが規定（固定値）の値と一致するか
  - ブロックの Hash 値が 1 つ前のブロックの Hash 値と一致すること
  - Proof of Work が一致すること
  - リワードトランザクションの送信者と金額が規定値と一致すること

Proof of Work（略「PoW」）とは

- ビットコインを初めとした暗号資産の取引や送金データを正しくブロックチェーン（block chain）につなぐための仕組み
- この実装では以下のとおり
  - ブロックのうちトランザクションリスト、ハッシュ値、ナンスのハッシュ値を求め、先頭４桁が`0000`であること
  - ブロック生成時は以下の通り
    - ハッシュ値計算対象のブロック内容
      - トランザクションリスト
      - ハッシュ値には最終ブロックのハッシュ値
      - ナンスは 0 から開始し 1 ずつ加算する
    - 上記ブロックのハッシュ値を求め、得られたハッシュ値の先頭 4 桁が`0000`となるまで繰り返す
  - ブロック検証時は以下の通り
    - ハッシュ値計算対象のブロック内容は受信したブロックそのもの
    - 上記ブロックのハッシュ値を求め、得られたハッシュ値の先頭 4 桁が`0000`であるか確認する
