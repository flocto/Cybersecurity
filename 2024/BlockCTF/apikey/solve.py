import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

data = '9Bmk+Nc8i7oz2+sRYI9Q1fZ/metvBlUzoMMdC2aLstA='
key = 'er34rgr3443.,g,3-09gjs@[wpef9j3j'

data = base64.b64decode(data)
key = key.encode()

c = AES.new(key, AES.MODE_ECB)

print(unpad(c.decrypt(data), AES.block_size).decode())