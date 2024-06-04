from pwn import *
from sage.all import *

# https://yondon.blog/2019/01/01/how-not-to-use-ecdsa/

context.log_level = 'critical'

p = 2**256 - 2**32 - 977
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
FF = GF(p)
EC = EllipticCurve([FF(0), FF(7)])
EC.set_order(n)

io = remote('13.38.208.179', int(11339))
# io = process(['python3', './src/app.py'])

io.recvuntil(b'G =')
G = EC(eval(io.recvline().strip().decode().replace(':', ',')))

io.recvuntil(b'H =')
H = EC(eval(io.recvline().strip().decode().replace(':', ',')))


"""
P = a*G + b*H

a = s^-1 * z
b = s^-1 * r

s = b^-1 * r = b^-1 * P.x
z = a * s = a * b^-1 * P.x

(r, s) = (P.x, P.x*b^-1)
"""

a = 2
b = 2

P = a*G + b*H

z = a * P.xy()[0] // b
r = P.xy()[0]
s = P.xy()[0] // b

io.sendlineafter(b'z > ', str(z).encode())
io.sendlineafter(b'r > ', str(r).encode())
io.sendlineafter(b's > ', str(s).encode())

print(io.recvall(timeout=1).decode().strip())