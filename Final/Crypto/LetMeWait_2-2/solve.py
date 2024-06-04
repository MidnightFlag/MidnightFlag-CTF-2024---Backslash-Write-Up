from pwn import *

context.log_level = 'critical'

def encrypt(letter: bytes, deepth: int=50) -> bytes:
	encrypt = hashlib.sha1(letter).hexdigest()
	for _ in range(deepth):
		encrypt = hashlib.sha1(encrypt.encode()).hexdigest()
	return encrypt

mapping = {encrypt(x.encode()): x for x in string.printable[:-5]}
charset = string.printable[:-5]

def guess_timing():
	results = []
	for i in range(10):
		before = time.time()
		io.sendlineafter(b'>', str(i).encode())
		r = io.recvline().strip().decode()
		delta = time.time() - before
		c = mapping[r]
		results.append((c, delta))
	return results

def filter_time(results, seuil=0.001):
	return [x[0] if x[1] < seuil else '' for x in results]

def bruteforce(results, i1, i2):
	for a in charset:
		for b in charset:
			x = results.copy()
			x[i1], x[i2] = a, b
			io.sendlineafter(b'>', ''.join(x).encode())
			r = io.recvline()
			if b'the token !' in r:
				continue
			print(r.decode().strip())
			exit()

while 1:
	io = remote('13.38.208.179', int(11019))
	results = filter_time(guess_timing(), seuil=0.001)
	if results.count('') == 2:
		i1 = results.index('')
		i2 = results[i1+1:].index('') + i1 + 1
		bruteforce(results, i1, i2)