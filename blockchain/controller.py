import os
from dotenv import load_dotenv
from fastapi import FastAPI
from blockchain.common import const, getAppLogger
from blockchain.model import Transaction, Chain
from blockchain.blockchain import BlockChain

logger = getAppLogger(__name__)
load_dotenv()
app = FastAPI()

blockchain = BlockChain()

# トランザクションプール参照機能
@app.get(const.URL_GET_TRANSACTION_POOL)
def get_transaction_pool():
  return blockchain.transaction_pool

# トランザクション登録・同報機能
@app.post(const.URL_REG_PUT_TRANSACTION)
def put_transaction(transaction: Transaction):
  if blockchain.verify_transaction(transaction):
    blockchain.add_transaction_pool(transaction)
    blockchain.broadcast_transaction(transaction)
    return editResponse("Transaction registered.")

# トランザクション同報更新機能
@app.post(const.URL_UPDATE_TRANSACTION)
def recieve_transaction(transaction: Transaction):
  if blockchain.verify_transaction(transaction):
    blockchain.add_transaction_pool(transaction)
    return editResponse("Transaction broadcasting completed.")

# ブロックチェーン参照機能
@app.get(const.URL_GET_CHAIN)
def get_chain():
  return blockchain.chain

# ブロック生成・ブロックチェーン同報機能
@app.get(const.URL_CREATE_BLOCK)
def create_block(creator: str):
  blockchain.create_block(creator)
  blockchain.broadcast_chain(blockchain.chain)
  return editResponse("New block generated.")

# ブロックチェーン同報更新機能
@app.post(const.URL_UPDATE_CHAIN)
def recieve_chain(chain: Chain):
  # 受信したブロックチェーンを検証する
  if blockchain.verify_chain(chain):
    blockchain.replace_chain(chain)
    return editResponse("BlockChain broadcasting completed.")
  else:
    return editResponse("BlockChain broadcasting uncompleted.")

# URL参照機能
@app.get(const.URL_GET_URL)
def view_url():
  return editResponse(blockchain.get_target_url())

def editResponse(message):
  logger.info(message)
  return {"message": message}