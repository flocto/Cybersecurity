from random import randint

N = 55
p = 7 
q = 1048576
d = 5 
h = [310887, 216621, -265484, 174500, -17777, -120033, 509794, 472383, -207899, 137579, -79499, -124308, -276940, 128084, -47635, -98217, -355596, 162484, 512568, 115895, 173988, -275814, 147875, 300084, -307229, 211325, -513412, 353600, 122876, -294850, -157799, -22315, 520548, -82043, 94241, -280271, -362973, 322837, 514352, 334680, -320170, 345083, 46507, -339191, 340263, 395440, -232497, 298320, 78618, -27607, -35665, -233166, 315029, -153394, -327546]
ciphertext_key = [9456, -87785, 54329, -52914, 192255, -362113, 192465, 207086, -299247, 33383, 323491, -56227, -256001, 183181, 347373, 199740, -142719, -155115, -234629, 367075, 83187, -434294, 30813, -288694, 487957, 173236, -426480, 322954, -316362, -284385, 33915, -193405, -378609, -345142, 62277, 52961, 370215, 383304, 179975, 287570, -254824, 306056, 33864, -480414, 41906, -387104, -504860, -17263, 15869, 47583, 128248, -71449, -225403, -458480, 514062]

def Zx(l):
    return list(l)

def gen_poly(d):
    res = N*[0]
    for j in range(d):  
        r = randint(0,N-1)
        while res[r] != 0:
            r = randint(0,N-1)
        res[r] = randint(-1,1)
    return Zx(res)
    
def gen_msg(d):
    return ZZ(list(randint(0,d-1)-2 for j in range(N)))

def encrypt(m, h): 
    r = gen_poly(d)
    return rangedmod(polymult(h,p*r) + m,q)

def generate_keys():
    while True:
        try:
            f = gen_poly(d)
            g = gen_poly(d)
            f_p = finvmodp(f,p)  
            f_q = finvmodp(f,q)
            secret_key = f, f_p
            h = rangedmod(p * polymult(f_q,g),q)
            break
        except:
            print("bad f and/or g, try again")
    
    return h,secret_key

print(gen_poly(d), gen_msg(d), encrypt(gen_msg(d), h), generate_keys())