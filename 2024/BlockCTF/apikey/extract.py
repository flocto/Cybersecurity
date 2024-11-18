from Crypto.Cipher import AES

key = b'gr3443.,g,3-s@[w'
data = open('8.data', 'rb').read()

c = AES.new(key, AES.MODE_ECB)

dec = c.decrypt(data)
open('8.dex', 'wb').write(dec)