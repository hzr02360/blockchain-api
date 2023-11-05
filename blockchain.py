# ブロックチェーンクラス
# ・トランザクション、ブロックを保持する
# ・トランザクション追加
# ・ブロック生成

import os
import requests
import json
import datetime
import config
from credential import convert_key_object, create_signeture

KEY_TRANSACTIONS = "transactions"
KEY_BLOCKS = "blocks"
REWORD_AMOUNT = 999

class BlockChain(object):

  # 初期処理
  def __init__(self):
    # トランザクション
    self.transaction_pool = {KEY_TRANSACTIONS: []}
    # ブロック
    self.chain = {KEY_BLOCKS: []}

  # 連携URL
  # ToDo 本番環境向けにリファクタ予定
  def get_target_url(self):
    urls = os.getenv("URL_TO_LINK")
    if urls:
      return urls.split(",")
    result = []
    current = os.getenv("CURRENT_URL")
    for target in config.URL_TO_LINK:
      if target.lower() != current.lower():
        result.append(target)
    return result

  # トランザクションプールにトランザクションを追加する
  def add_transaction_pool(self, transaction):
    transaction_dict = transaction.dict()
    self.transaction_pool[KEY_TRANSACTIONS].append(transaction_dict)

  # ブロック生成
  def create_block(self, creator):
    # リワードトランザクション
    reword_transactuin_dict = {
      "time": datetime.datetime.now().isoformat(),
      "sender": "BlockChain",
      "reciever": creator,
      "amount": REWORD_AMOUNT,
      "description": "reword",
      "signature": "not required"
    }
    # リワードトランザクションを登録する
    transactions = self.transaction_pool[KEY_TRANSACTIONS]
    transactions.append(reword_transactuin_dict)
    # ブロックを生成しチェーンへ追加する
    block = {
      "time": datetime.datetime.now().isoformat(),
      "transactions": transactions,
      "hash": "Temporary hash value",
      "nonce": 0      
    }
    self.chain[KEY_BLOCKS].append(block)
    # トランザクションプール初期化
    self.transaction_pool[KEY_TRANSACTIONS] = []

  # トランザクション連携
  def broadcast_transaction(self, transaction):
    transaction_dict = transaction.dict()
    for url in self.get_target_url():
      res = requests.post(url + "/recieve_transaction", json.dumps(transaction_dict))
      print(res.json())

  # ブロックチェーン連携
  def broadcast_chain(self, chain):
    for url in self.get_target_url():
      res = requests.post(url + "/recieve_chain", json.dumps(chain))
      print(res.json())

  # ブロックチェーン交換
  def replace_chain(self, chain):
    chain_dict = chain.dict()
    self.chain = chain_dict
    self.transaction_pool[KEY_TRANSACTIONS] = []

  # トランザクションデータ検証
  def verify_transaction(self, transaction):
    pub_key = convert_key_object(transaction.sender)
    signature_str = create_signeture(transaction.signature)
    unsigned_tran = {
      "time": transaction.time,
      "sender": transaction.sender,
      "reciever": transaction.reciever,
      "amount": transaction.amount,
      "description": transaction.description
    }
    json_unsigned_tran = json.dumps(unsigned_tran)
    bytes_unsigned_tran = bytes(json_unsigned_tran, encoding="utf-8")
    return pub_key.verify(signature_str, bytes_unsigned_tran)

