

# This file was *autogenerated* from the file test.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff = Integer(0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff); _sage_const_0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296 = Integer(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296); _sage_const_0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5 = Integer(0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5); _sage_const_0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551 = Integer(0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551); _sage_const_0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc = Integer(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc); _sage_const_0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b = Integer(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b)
p = _sage_const_0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff 
Gx = _sage_const_0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296 
Gy = _sage_const_0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5 
q = _sage_const_0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551 

a = _sage_const_0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc 
b = _sage_const_0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b 

# p256 curve
E = EllipticCurve(GF(p), [a, b], order=q)

G = E(Gx, Gy)

print(G.order(), hex(G.order()))
