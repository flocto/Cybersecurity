from hashlib import sha1, md5

def hex_byte_to_int(c):
    if c >= 0x30 and c <= 0x39:
        return c - 0x30
    else:
        return c - 0x37

chars = []
arena = open('arena.tscn', 'r').read().split('\n')[151:]
for i in range(30):
    chunk = arena[i*9:i*9+9]
    x = float(chunk[1].split()[-1])
    y = float(chunk[2].split()[-1])
    text = eval(chunk[5].split()[-1])
    # print(x, y, text)
    chars.append((x, y, text))

S = 50
for i in range(2**10):
    b = bin(i)[2:].zfill(10)
    sha = sha1(b.encode()).hexdigest().upper().encode()
    sha += md5(b.encode()).hexdigest().upper().encode()
    # print(sha, len(sha))

    X, Y = [], []
    for i in range(30):
        X.append(hex_byte_to_int(sha[i * 2]) - 8)
        Y.append(hex_byte_to_int(sha[i * 2 + 1]) - 8)

    chars_moved = []
    for i, (x, y, text) in enumerate(chars):
        chars_moved.append((x + X[i] * S, y + Y[i] * S, text))
    
    chars_moved_y = [y for x, y, text in chars_moved]
    if max(chars_moved_y) - min(chars_moved_y) < 100:
        # print(b)
        chars_moved.sort(key=lambda x: x[0])
        print(''.join([text for x, y, text in chars_moved]))
