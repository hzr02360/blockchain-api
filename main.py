# ブロックチェーンAPIサーバの主処理
from fastapi import FastAPI
import blockchain
from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
  time: str
  sender: str
  reciever: str
  amount: int
  description: str
  signature: str

class Block(BaseModel):
  time: str
  transactions: List[Transaction]
  hash: str
  nonce: int

class Chain(BaseModel):
  blocks: List[Block]

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

# トランザクション登録・同報機能
@app.post("/put_transaction")
def put_transaction(transaction: Transaction):
  blockchain.add_transaction_pool(transaction)
  blockchain.broadcast_transaction(transaction)
  return {"message": "Transaction registered."}

# ブロック生成・同報機能
@app.get("/create_block/{creator}")
def create_block(creator: str):
  blockchain.create_block(creator)
  blockchain.broadcast_chain(blockchain.chain)
  return {"message": "New block generated."}

# トランザクション更新機能
@app.post("/recieve_transaction")
def recieve_transaction(transaction: Transaction):
  blockchain.add_transaction_pool(transaction)
  return {"message": "Transaction broadcasting completed."}

# ブロックチェーン更新機能
@app.post("/recieve_chain")
def recieve_chain(chain: Chain):
  blockchain.replace_chain(chain)
  return {"message": "BlockChain broadcasting completed."}

@app.get("/url")
def view_url():
  return {"message": blockchain.get_target_url()}