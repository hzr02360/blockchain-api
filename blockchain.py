# ブロックチェーンクラス
# ・トランザクション、ブロックを保持する
# ・トランザクション追加
# ・ブロック生成

import os
import requests
import json
import datetime
import config
import hashlib

from credential import convert_key_object, create_signeture

KEY_TRANSACTIONS = "transactions"
KEY_BLOCKS = "blocks"
KEY_HASH = "hash"
KEY_NONCE = "nonce"
REWORD_AMOUNT = 999
POW_DIGIT = 4

class BlockChain(object):

  # 初期処理
  def __init__(self):
    # トランザクション
    self.transaction_pool = {KEY_TRANSACTIONS: []}
    # ブロック
    self.chain = {KEY_BLOCKS: []}
    # 1件目のブロックを生成する
    self.first_block = {
      "time": "0000-00-00T00:00:00.000000",
      "transactions": [],
      "hash": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "nonce": 0
    }
    self.chain[KEY_BLOCKS].append(self.first_block)

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
    transactions = self.transaction_pool[KEY_TRANSACTIONS].copy()
    transactions.append(reword_transactuin_dict)
    # 最後のブロックのハッシュを生成する
    last_block = self.chain[KEY_BLOCKS][-1]
    hash = self.hash(last_block)
    # Proof of workのためのハッシュ値計算
    pow_block = {
      "transactions": transactions,
      "hash": hash,
      "nonce": 0      
    }
    while not self.hash(pow_block)[:POW_DIGIT] == '0'*POW_DIGIT:
      pow_block[KEY_NONCE] += 1
    # ブロックを生成しチェーンへ追加する
    block = {
      "time": datetime.datetime.now().isoformat(),
      "transactions": pow_block[KEY_TRANSACTIONS],
      "hash": pow_block[KEY_HASH],
      "nonce": pow_block[KEY_NONCE]     
    }
    self.chain[KEY_BLOCKS].append(block)
    # トランザクションプール初期化
    # 新しいブロックが含んでいるトランザクションデータをトランザクションプールから削除する
    for transaction in block[KEY_TRANSACTIONS]:
      if transaction in self.transaction_pool[KEY_TRANSACTIONS]:
        self.transaction_pool[KEY_TRANSACTIONS].remove(transaction)

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
    # トランザクションプール初期化
    # 受け取ったブロックチェーンの最終ブロックが含んでいるトランザクションデータをトランザクションプールから削除する
    last_block_transaction = self.chain[KEY_BLOCKS][-1][KEY_TRANSACTIONS]
    for transaction in last_block_transaction:
      if transaction in self.transaction_pool[KEY_TRANSACTIONS]:
        self.transaction_pool[KEY_TRANSACTIONS].remove(transaction)

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

  # ハッシュ生成
  def hash(self, block):
    json_block = json.dumps(block)
    byte_block = bytes(json_block, encoding="utf-8")
    return hashlib.sha256(byte_block).hexdigest()
