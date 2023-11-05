# ブロックチェーンAPIサーバの主処理
from fastapi import FastAPI
from model import Transaction, Chain
import blockchain

app = FastAPI()

blockchain = blockchain.BlockChain()

# トランザクションプール参照機能
@app.get("/get_transaction_pool")
def get_transaction_pool():
  return blockchain.transaction_pool

# トランザクション登録・同報機能
@app.post("/put_transaction")
def put_transaction(transaction: Transaction):
  if blockchain.verify_transaction(transaction):
    blockchain.add_transaction_pool(transaction)
    blockchain.broadcast_transaction(transaction)
    return {"message": "Transaction registered."}

# トランザクション同報更新機能
@app.post("/recieve_transaction")
def recieve_transaction(transaction: Transaction):
  if blockchain.verify_transaction(transaction):
    blockchain.add_transaction_pool(transaction)
    return {"message": "Transaction broadcasting completed."}

# ブロックチェーン参照機能
@app.get("/get_chain")
def get_chain():
  return blockchain.chain

# ブロック生成・ブロックチェーン同報機能
@app.get("/create_block/{creator}")
def create_block(creator: str):
  blockchain.create_block(creator)
  blockchain.broadcast_chain(blockchain.chain)
  return {"message": "New block generated."}

# ブロックチェーン同報更新機能
@app.post("/recieve_chain")
def recieve_chain(chain: Chain):
  blockchain.replace_chain(chain)
  return {"message": "BlockChain broadcasting completed."}

# URL参照機能
@app.get("/url")
def view_url():
  return {"message": blockchain.get_target_url()}