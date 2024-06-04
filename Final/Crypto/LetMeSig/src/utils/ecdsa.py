from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from base64 import b64decode, b64encode
from random import randint
import hashlib
import sys, os

from sage.all import *

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
secp256r1 = EllipticCurve(GF(p),[
    0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc, 
    0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
])
G = secp256r1(  0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 
                0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)


class NonceGenerator:
	def __init__(self, seed, n):
		self.secret = list(seed)
		self.n = n

	def xor(self, a, b):
		return bytes([x^y for x, y in zip(a, b)])

	def update_secret(self, k):
		for _ in range(k):
			idx = randint( (len(self.secret)-1) // 2, len(self.secret)-1)
			new = randint(0,255)
			self.secret[idx] = new

	def next(self, m):
		h = hashlib.sha256(m.strip()).digest()
		self.update_secret(k=10)
		return bytes_to_long(self.xor(h, self.secret)) % self.n



class ECDSA:
	def __init__(self, curve, base, secret):
		self.E = curve
		self.G = base
		self.n = self.E.order()
		self.generator = NonceGenerator(seed=secret, n=self.n)
		self.d = randint(1, self.n-1)
		self.Q = self.d * self.G

	def pack(self, r, s):
		return b64encode(f'{r}|{s}'.encode()).decode()

	def unpack(self, sig):
		return [int(x) for x in b64decode(sig.encode()).decode().split('|')[:2]]

	def refresh_nonce(self, message):
		self.k = self.generator.next(message)

	def hash(self, message):
		return bytes_to_long(hashlib.sha1(message).digest())

	def sign(self, msg):
		# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
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

	def verify(self, sig, msg):
		try:
			r, s = self.unpack(sig)
			h = self.hash(msg)

			if not (0 < r < self.n - 1):
				return False

			if not (0 < s < self.n - 1):
				return False 

			u1 = int(h * inverse(s, self.n) % self.n)
			u2 = int(r * inverse(s, self.n) % self.n)

			P = u1 * self.G + u2 * self.Q

			return P.xy()[0] == r % self.n
		except Exception as ex:
			print(ex)
			return False


ecdsa = ECDSA(
	curve=secp256r1,
	base=G, 
	secret=os.urandom(32)
)