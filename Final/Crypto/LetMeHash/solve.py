from sage.all import *

from pwn import *
from os import urandom
from Crypto.Util.number import long_to_bytes, bytes_to_long

context.log_level = 'critical'

class Client:
	def __init__(self, ip, port):
		self.io = remote(ip, int(port))

	def shell(self):
		self.io.interactive()

	def hash(self, message):
		self.io.sendlineafter(b'msg = ', message.hex().encode())
		hash_ = int(self.io.recvline().strip().decode())
		return hash_

	def submit(self, message):
		self.io.sendlineafter(b'msg = ', b'')
		self.io.recvline()
		self.io.sendlineafter(b'Did you learn something? ', message.hex().encode())
		result = self.io.recvline().strip()
		return b'Nice one' in result


class hash_xor_collider:
	def __init__(self, hash_func, bitlength:int, msg_len: int=32, K:int=200):
		self.h = hash_func
		self.bitlength = bitlength
		self.msg_len = msg_len
		self.K = K

	def search(self, target: int) -> list[bytes]:
		matrix, messages = self.generate_matrix()
		sol = self.solve_matrix(matrix, target)
		if not sol:
			return [], b''

		S = []
		for i, x in enumerate(sol):
			if x == 1:
				S.append(bytes.fromhex(messages[i].hex()))
		r = 0
		for m in S:
			r ^= self.h(m)

		assert r == target
		return S

	def generate_matrix(self) -> (Matrix, list):
		M = []
		m = []
		for _ in range(self.K):
			msg = urandom(self.msg_len)
			m.append(msg)
			M.append([int(b) for b in format(self.h(msg), '0%sb'%str(self.bitlength))])
		return Matrix(GF(2), M).transpose(), m

	def solve_matrix(self, M: Matrix, target: int):
		try:
			solution = M.solve_right(vector(GF(2), format(target, '0%sb'%str(self.bitlength))))
			return [int(x) for x in solution]
		except ValueError:
			return None

def get_target_crc(target: bytes) -> int:
	A = urandom(len(target))
	B = urandom(len(target))
	C = xor(xor(A,B), target)
	crc_target = io.hash(A) ^ io.hash(B) ^ io.hash(C)
	return crc_target

def xor(A, B):
	return bytes([a ^ b for a, b in zip(A, B)])

def my_hash(inp: bytes) -> int:
	return io.hash(inp)

io = Client('13.38.208.179', int(10058))

c = hash_xor_collider(
	hash_func=my_hash,
	bitlength=32,
	msg_len=32,
	K=75
)

cpt = 0
K = 200

while cpt < K:
	print(f'{str(cpt)}/{str(K)}', end='\r')

	crc_target = get_target_crc(b'Sign me')
	L = c.search(target=crc_target)

	payload = b'\x00'*32
	for x in L:
		payload = xor(payload, x)

	if crc_target == my_hash(payload):
		assert io.submit(payload)
		cpt += 1

io.shell()