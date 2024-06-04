from sage.all import *
import random, os

flag = os.getenv('FLAG', 'flag{ThisIsTheFlag}')

# secp256k1 Curve
p = 2**256 - 2**32 - 977
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
FF = GF(p)
EC = EllipticCurve([FF(0), FF(7)])
EC.set_order(n)

# Challenge
G = EC.random_point()
print("G =", G)

secret = random.randrange(p)
H = G * secret
print("H =", H)

print("Are you god ?")
z = int(input("z > "))
r = int(input("r > "))
s = int(input("s > "))

assert n // 1000 < z < n, 'No flag for you'
assert n // 1000 < r < n, 'No flag for you'
assert n // 1000 < s < n, 'No flag for you'

w = pow(s, -1, n)
u1 = (z * w) % n
u2 = (r * w) % n

v = (u1 * G) + (u2 * H)

assert r == int(v.xy()[0]) % n, 'No flag for you'

print(f'Well done ! Here is the flag: {flag}')
