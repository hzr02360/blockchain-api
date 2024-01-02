import os
import inspect
import requests
import json
import datetime
import hashlib
from blockchain.common import const, getAppLogger, convert_key_object, create_signeture

KEY_TRANSACTIONS = "transactions"
KEY_BLOCKS = "blocks"
KEY_HASH = "hash"
KEY_NONCE = "nonce"
KEY_TIME = "time"
KEY_SENDER = "sender"
KEY_RECIEVER = "reciever"
KEY_AMOUNT = "amount"
KEY_DESCRIPTION = "description"
KEY_SIGNATURE = "signature"
REWORD_AMOUNT = 999
POW_DIGIT = 4

logger = getAppLogger(__name__)

class BlockChain(object):

  # 初期処理
  def __init__(self):
    # トランザクション
    self.transaction_pool = {KEY_TRANSACTIONS: []}
    # ブロック
    self.chain = {KEY_BLOCKS: []}
    # 1件目のブロックを生成する
    self.first_block = {
      KEY_TIME: "0000-00-00T00:00:00.000000",
      KEY_TRANSACTIONS: [],
      KEY_HASH: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      KEY_NONCE: 0
    }
    self.chain[KEY_BLOCKS].append(self.first_block)

  # 連携URL
  def get_target_url(self):
    urls = os.getenv("URL_TO_LINK")
    return urls.split(",")

  # トランザクションプールにトランザクションを追加する
  def add_transaction_pool(self, transaction):
    transaction_dict = transaction.dict()
    self.transaction_pool[KEY_TRANSACTIONS].append(transaction_dict)

  # ブロック生成
  def create_block(self, creator):
    # リワードトランザクション
    reword_transactuin_dict = {
      KEY_TIME: datetime.datetime.now().isoformat(),
      KEY_SENDER: "BlockChain",
      KEY_RECIEVER: creator,
      KEY_AMOUNT: REWORD_AMOUNT,
      KEY_DESCRIPTION: "reword",
      KEY_SIGNATURE: "not required"
    }
    # リワードトランザクションを登録する
    transactions = self.transaction_pool[KEY_TRANSACTIONS].copy()
    transactions.append(reword_transactuin_dict)
    # 最後のブロックのハッシュを生成する
    last_block = self.chain[KEY_BLOCKS][-1]
    hash = self.hash(last_block)
    # Proof of workのためのハッシュ値計算
    pow_block = {
      KEY_TRANSACTIONS: transactions,
      KEY_HASH: hash,
      KEY_NONCE: 0      
    }
    while not self.hash(pow_block)[:POW_DIGIT] == '0'*POW_DIGIT:
      pow_block[KEY_NONCE] += 1
    # ブロックを生成しチェーンへ追加する
    block = {
      KEY_TIME: datetime.datetime.now().isoformat(),
      KEY_TRANSACTIONS: pow_block[KEY_TRANSACTIONS],
      KEY_HASH: pow_block[KEY_HASH],
      KEY_NONCE: pow_block[KEY_NONCE]     
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
      res = requests.post(url + const.URL_UPDATE_TRANSACTION, json.dumps(transaction_dict))
      logger.info('%s:%s,%s', inspect.currentframe().f_code.co_name, url.replace('\n', ''), res.json())

  # ブロックチェーン連携
  def broadcast_chain(self, chain):
    for url in self.get_target_url():
      res = requests.post(url + const.URL_UPDATE_CHAIN, json.dumps(chain))
      logger.info('%s:%s,%s', inspect.currentframe().f_code.co_name, url.replace('\n', ''), res.json())

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
      KEY_TIME: transaction.time,
      KEY_SENDER: transaction.sender,
      KEY_RECIEVER: transaction.reciever,
      KEY_AMOUNT: transaction.amount,
      KEY_DESCRIPTION: transaction.description
    }
    json_unsigned_tran = json.dumps(unsigned_tran)
    bytes_unsigned_tran = bytes(json_unsigned_tran, encoding="utf-8")
    return pub_key.verify(signature_str, bytes_unsigned_tran)

  # ブロックチェーン検証
  def verify_chain(self, chain):
    chain_dict = chain.dict()
    # ブロック数を検証する
    if len(chain_dict[KEY_BLOCKS]) <= len(self.chain[KEY_BLOCKS]):
      return False

    # 全ブロックを検証する
    for i in range(len(chain_dict[KEY_BLOCKS])):
      block = chain_dict[KEY_BLOCKS][i]
      prev_block = chain_dict[KEY_BLOCKS][i - 1]
      if i == 0:
        # 先頭ブロックが初期値と一致することを確認する
        if block != self.first_block:
          return False
      else:
        # ブロックのHash値が1つ前のブロックのHash値と一致することを確認する
        if (block[KEY_HASH] != self.hash(prev_block)):
          return False
        # Proof of Workを確認する
        # transactions, hash, nonceの結合情報のHash値の先頭4桁が0000であること
        block_without_time = {
          KEY_TRANSACTIONS: block[KEY_TRANSACTIONS],
          KEY_HASH: block[KEY_HASH],
          KEY_NONCE: block[KEY_NONCE]
        }
        if self.hash(block_without_time)[:POW_DIGIT] != '0'*POW_DIGIT:
          return False

    # リワードトランザクションを検証する
    # sender, amountが一致していること
    reword_transaction = chain_dict[KEY_BLOCKS][-1][KEY_TRANSACTIONS][-1]
    if reword_transaction[KEY_SENDER] != "Blockchain":
      return False
    if reword_transaction[KEY_AMOUNT] != REWORD_AMOUNT:
      return False

    return True

  # ハッシュ生成
  def hash(self, block):
    json_block = json.dumps(block)
    byte_block = bytes(json_block, encoding="utf-8")
    return hashlib.sha256(byte_block).hexdigest()
