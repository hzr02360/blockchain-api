# ブロックチェーンAPIサーバの主処理
from fastapi import FastAPI
import blockchain

from pydantic import BaseModel

class Transaction(BaseModel):
  time: str
  sender: str
  reciever: str
  amount: int
  description: str
  signature: str

blockchain = blockchain.BlockChain()

app = FastAPI()

# トランザクションプール参照機能
@app.get("/get_transaction_pool")
def get_transaction_pool():
  return blockchain.transaction_pool

# チェーン参照機能
@app.get("/get_chain")
def get_chain():
  return blockchain.chain

# トランザクション登録機能
@app.post("/put_transaction")
def put_transaction(transaction: Transaction):
  blockchain.add_transaction_pool(transaction)
  return {"message": "Transaction registered."}

# ブロック生成機能
@app.get("/create_block/{creator}")
def create_block(creator: str):
  blockchain.create_block(creator)
  return {"message": "New block generated."}