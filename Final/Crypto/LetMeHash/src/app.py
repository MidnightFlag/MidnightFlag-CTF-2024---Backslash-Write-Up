import os, re
import signal

# Avoid bruteforce
signal.alarm(60 * 10) 

class CRC32:
	def __init__(self):
		self.polynomial = 0xEDB88320
		self.crc = self.gen_initial_state()
		self.init_table()

	def gen_initial_state(self):
		return int.from_bytes(os.urandom(4), byteorder="big")


	def init_table(self) -> None:
		self.table = []
		for i in range(256):
			for _ in range(8):
				i = i >> 1 ^ self.polynomial if i & 1 else i >> 1
			self.table.append(i)

	def hash(self, data: bytes) -> int:
		crc = self.crc
		for c in data:
			crc = self.table[(crc ^ c) & 0xFF] ^ (crc >> 8)
		return crc ^ 0xFFFFFFFF



class Challenge:
	def __init__(self, C: int, target: bytes, secret: str) -> None:
		self.num_of_win = C
		self.sign_me = target
		self.secret = secret
		self.win = 0

	def is_hex(self, s):
		charset = re.fullmatch(r"^[0-9a-fA-F]+$", s or "") is not None
		length = len(s)%2 == 0
		return charset and length

	def round(self, k):
		while 1:
			msg = input(f"Round N°{k} | msg = ").strip()

			if not self.is_hex(msg):
				print(f'Round N°{k} | Malformed input !')
				break

			print(self.crc.hash(data=bytes.fromhex(msg)))

		sol = input(f"Round N°{k} | Did you learn something? ")

		if not self.is_hex(sol):
			return f'Round N°{k} | Malformed input !'

		msg = bytes.fromhex(sol)

		if msg == self.sign_me and 1==2:
			return f'Round N°{k} | Forbidden input !'

		elif self.crc.hash(data=msg) != self.crc.hash(self.sign_me):
			return f'Round N°{k} | CRC32 differents !'

		else:
			self.win += 1
			return f'Round N°{k} | Nice one :D'

	def run(self):
		for k in range(1, self.num_of_win+1):
			self.crc = CRC32()
			result = self.round(k=k)
			print(result)

		if self.num_of_win != self.win:
			print(f'You missed at least one')
		else:
			print(f"GG, the flag is {self.secret}")
		

c = Challenge(
	C=200,
	target=b'Sign me',
	secret=os.getenv('FLAG', 'flag{ThisIs@F4keFlag!}')
)
c.run()