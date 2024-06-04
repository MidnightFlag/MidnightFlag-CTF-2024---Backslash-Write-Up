from sage.all import *

from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long
from base64 import b64decode, b64encode
import requests
import re
import random
import hashlib
import os

def ecdsa_biased_nonce_shared_msb(Z, R, S, n, l):
	# https://github.com/josephsurin/lattice-based-cryptanalysis/blob/main/tutorial.pdf
	def hnp(p, T, A, B):
		m = len(T)
		M = p * Matrix.identity(QQ, m)
		M = M.stack(vector(T))
		M = M.stack(vector(A))
		M = M.augment(vector([0] * m + [B / p] + [0]))
		M = M.augment(vector([0] * (m + 1) + [B]))
		M = M.dense_matrix()

		M = M.LLL()
		
		for row in M:
			if row[-1] == -B:
				alpha = (row[-2] * p / B) % p
				if all((beta - t * alpha + a) % p == 0 for beta, t, a in zip(row[:m], T, A)):
					return alpha
			if row[-1] == B:
				alpha = (-row[-2] * p / B) % p
				if all((beta - t * alpha + a) % p == 0 for beta, t, a in zip(-row[:m], T, A)):
					return alpha
		return None

	z1, r1, s1 = Z[0], R[0], S[0]
	T = [ZZ((pow(s, -1, n) * r - pow(s1, -1, n) * r1) % n) for s, r in zip(S[1:], R[1:])]
	A = [ZZ((pow(s1, -1, n) * z1 - pow(s, -1, n) * z) % n) for s, z in zip(S[1:], Z[1:])]
	B = 2^(n.nbits() - l)
	d = hnp(n, T, A, B)
	return d

def unpack(sig):
	return [int(x) for x in b64decode(sig.encode()).decode().split('|')[:2]]

def hash_(message):
	return bytes_to_long(hashlib.sha1(message).digest())

class ECDSA:
	def __init__(self, curve, base, d):
		self.E = curve
		self.G = base
		self.n = self.E.order()
		self.d = d
		self.Q = self.d * self.G

	def pack(self, r, s):
		return b64encode(f'{r}|{s}'.encode()).decode()

	def unpack(self, sig):
		return [int(x) for x in b64decode(sig.encode()).decode().split('|')[:2]]

	def refresh_nonce(self, message):
		self.k = 35

	def hash(self, message):
		return bytes_to_long(hashlib.sha1(message).digest())

	def sign(self, msg):
		h = self.hash(msg)
		while 1:
			self.refresh_nonce(msg)
			P = self.k * self.G
			r = int(P.xy()[0]) % self.n
			if not r:
				continue
			s = (h + r * self.d) * inverse(self.k, self.n) % self.n
			if not s:
				continue
			return self.pack(r, s)


class Client:
	def __init__(self, url):
		self.url = url
		self.s = requests.session()

	def register(self, username):
		res = self.s.post(f'{self.url}/register', data={'username': username}).text
		sig = re.findall(r'<li class="list-group-item">(.*?)</li>', res)
		return sig[1]

	def login(self, username, signature):
		res = self.s.post(f'{self.url}/login', data={'username': username, 'signature': signature})
		return res.text



###### CURVE ######
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
secp256r1 = EllipticCurve(GF(p),[
    0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc, 
    0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
])
G = secp256r1(  0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 
                0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)


K = 15


users = [''.join([random.choice('abcdefghijklmopqrstuvwxyz') for _ in range(5)])]
for _ in range(K):
	users.append(users[-1] + " ")


Z, R, S = [], [], []

n = Integer(secp256r1.order())
l = Integer(128) # MSB partagé de 128 bits

c = Client(url='http://172.18.229.196:5000')

for U in users:
	z = hash_(U.encode())
	r, s = unpack(c.register(username=U))
	Z.append(ZZ(z))
	R.append(ZZ(r))
	S.append(ZZ(s))


d = ecdsa_biased_nonce_shared_msb(Z, R, S, n, l)
print(f'Private key: {str(d)}')

ecdsa  = ECDSA(curve=secp256r1, base=G, d=d)
sig = ecdsa.sign(msg=b'admin')
print(f'Signature: {str(sig)}')


result = c.login(username='admin', signature=sig)
print('Result: ')
print(result)