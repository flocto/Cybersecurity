from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

key = 'qQwrmkzuhJv6fzCF2XsxuaB+ZBtMEH+Cd3fpTgJpEM8='
iv = 'FjmNRmlNzMZYK8TbIItuVA=='
enc = '8XvXFKhm8YFfQShtVXcNZh5F8q0zBJMTnfBSh33SEr8r4hMWb/E2VJq20QO2Byef'

key = base64.b64decode(key)
iv = base64.b64decode(iv)
enc = base64.b64decode(enc)

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = cipher.decrypt(enc)

print(unpad(flag, 16).decode())