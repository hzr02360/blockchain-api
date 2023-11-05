# データモデル定義
from pydantic import BaseModel
from typing import List

# トランザクション
class Transaction(BaseModel):
  time: str
  sender: str
  reciever: str
  amount: int
  description: str
  signature: str

# ブロック
class Block(BaseModel):
  time: str
  transactions: List[Transaction]
  hash: str
  nonce: int

# ブロックチェーン
class Chain(BaseModel):
  blocks: List[Block]
