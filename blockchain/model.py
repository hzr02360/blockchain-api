# データモデル定義
from pydantic import BaseModel
from typing import List

# トランザクション
class Transaction(BaseModel):
  time: str # タイムスタンプ
  sender: str # 送金者
  reciever: str # 受取人
  amount: int # 金額
  description: str # 説明
  signature: str # シグネチャ

# ブロック
class Block(BaseModel):
  time: str # タイムスタンプ
  transactions: List[Transaction] # トランザクションリスト
  hash: str # 1つ前のブロックのハッシュ
  nonce: int # nonce

# ブロックチェーン
class Chain(BaseModel):
  blocks: List[Block] # ブロックリスト
