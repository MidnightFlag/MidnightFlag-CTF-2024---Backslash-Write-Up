from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, getPrime
from functools import reduce
from sympy import nextprime
from random import randint

class MRSA():
	def __init__(self, bitlength: int=2048, primes: int=4) -> None:
		self.bl = bitlength
		self.c = primes
		self.generate_keys()

	def generate_keys(self) -> None:
		def random_nbit_int(l):
			return randint(2**(l-1),2**l)

		def gen_primes() -> list[int]:
			primes = []
			l1 = int((self.bl // self.c) * 1/4)
			l2 = int((self.bl // self.c) - l1)
			base = random_nbit_int(l1)
			for k in range(self.c):
				primes.append(nextprime(2**l2*base + random_nbit_int(l2)))
			return primes

		self.primes = gen_primes()		
		self.n = reduce(lambda x, y: x * y, self.primes)

		self.phi = 1
		for p in self.primes:
			self.phi *= (p-1)

		self.d = nextprime(random_nbit_int(int(self.n.bit_length()*0.15)))
		self.e = pow(self.d,-1,self.phi)

	def get_publickey(self) -> tuple[int, int]:
		return (self.e,self.n)

	def get_privatekey(self) -> int:
		return self.d

	def encrypt(self,message: bytes) -> int:
		return pow(bytes_to_long(message),self.e,self.n)

	def decrypt(self,message: int) -> bytes:
		return long_to_bytes(pow(message,self.d,self.n))


rsa = MRSA(
	bitlength=2048,
	primes=5
)

e, n = rsa.get_publickey()
m = b'ESNA{ThisisAFakeFlag}'
c = rsa.encrypt(m)

print(f'''
e={e}
n={n}
c={c}
'''.strip())