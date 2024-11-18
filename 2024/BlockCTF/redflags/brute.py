from hashlib import sha1, md5

def hex_byte_to_int(c):
    if c >= 0x30 and c <= 0x39:
        return c - 0x30
    else:
        return c - 0x37


for i in range(2**10):
    b = bin(i)[2:].zfill(10)
    sha = sha1(b.encode()).hexdigest().upper().encode()
    sha += md5(b.encode()).hexdigest().upper().encode()
    print(sha, len(sha))

    X, Y = [], []
    for i in range(30):
        X.append(hex_byte_to_int(sha[i * 2])  - 8)
        Y.append(hex_byte_to_int(sha[i * 2 + 1])  - 8)

    if len(set(Y)) < 10 or len(set(X)) < 10:
        print(X, Y, b)