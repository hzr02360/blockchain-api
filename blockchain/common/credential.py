from ecdsa import VerifyingKey
from ecdsa import SECP256k1
import binascii

# 公開鍵をKeyオブジェクトに変換する
def convert_key_object(pub_key):
  return VerifyingKey.from_string(binascii.unhexlify(pub_key), curve=SECP256k1)

# シグネチャを生成する
def create_signeture(signature):
  return binascii.unhexlify(signature)