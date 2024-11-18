from ctypes import CDLL
import datetime
from Crypto.Cipher import AES

libc = CDLL("libc.so.6")

def generate_random_bytes(seed, n):
    libc.srand(seed)
    result = b""

    # for _ in range(n):
    #     x0_1 = libc.rand()
    #     x1 = -x0_1

    #     if x1 < 0:
    #         x2_1 = x0_1 & 0xff
    #     else:
    #         x2_1 = (-x1 & 0xff)

    #     result += bytes([x2_1 & 0xff])
    result = bytes([libc.rand() & 0xff for _ in range(n)])
    
    return result

# 2024-10-23 19:59:04
time = datetime.datetime(2024, 10, 23, 19, 59, 4)
time = round(time.timestamp())

key = generate_random_bytes(time, 32)
iv = generate_random_bytes(time, 16)
enc = open('flag.txt.enc', 'rb').read()

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = cipher.decrypt(enc)
print(flag.decode())