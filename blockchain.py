# ブロックチェーンクラス
# ・トランザクション、ブロックを保持する
# ・トランザクション追加
# ・ブロック生成

import datetime

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

