import sys


def enigma(plain_text, offset1, offset2, offset3):
    # Rotation mappings provided in the function
    map1 = "YKNQXBMOVZPIAEJCSDLGRTUFWH"
    map2 = "ZXVALNTFMJQBCPYWURSOKDEHIG"
    map3 = "RETAIGBSJNUWYXZLPVKCDMQOFH"
    map4 = "YGQNVUBROLTJZDIWCHXKFEPSAM"

    # Initial offset values, assuming they start at zero for encryption
    encrypted_text = []

    for char in plain_text:
        char = map1[(offset1 + ord(char) - ord('A')) % 26]
        char = map2[(offset2 + ord(char) - ord('A')) % 26]
        char = map3[(offset3 + ord(char) - ord('A')) % 26]
        char = map4[ord(char) - ord('A')]

        for i in range(26):
            if map3[i] == char:
                char = chr(((i - offset3 + 26) % 26) + 65)
                break

        for i in range(26):
            if map2[i] == char:
                char = chr(((i - offset2 + 26) % 26) + 65)
                break

        for i in range(26):
            if map1[i] == char:
                char = chr(((i - offset1 + 26) % 26) + 65)
                break

        # Append the encrypted character
        encrypted_text.append(char)

        # Rotate offsets like an Enigma machine
        offset1 = (offset1 + 1) % 26
        if offset1 == 0:
            offset2 = (offset2 + 1) % 26
            if offset2 == 0:
                offset3 = (offset3 + 1) % 26

    return ''.join(encrypted_text)


# Test with an encrypted message
encrypted_message = "FLAG"
enc = "KKPEFJZBSVNBYWWOKOJIPNWGPGASCVVYPAYLAHTX"
print(enigma(enc, 7, 7, 4))
