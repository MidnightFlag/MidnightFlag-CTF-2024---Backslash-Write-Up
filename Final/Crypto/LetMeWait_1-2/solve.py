from pwn import *

context.log_level = 'critical'

io = remote('13.38.208.179', int(11864))
# io = process(['python3', './src/app.py'])

def encrypt(letter: bytes, deepth: int=50) -> bytes:
	encrypt = hashlib.sha1(letter).hexdigest()
	for _ in range(deepth):
		encrypt = hashlib.sha1(encrypt.encode()).hexdigest()
	return encrypt

mapping = {encrypt(x.encode()): x for x in string.printable[:-5]}

results = [{} for _ in range(20)]

for i in range(20):
	for _ in range(20):
		io.sendlineafter(b'>', str(i).encode())
		r = io.recvline().strip().decode()
		c = mapping[r]
		if c in results[i]:
			results[i][c] += 1
		else:
			results[i][c] = 1

results = [sorted(dico.items(), key=lambda x:x[1]) for dico in results]
token = ''.join([dico[-1][0] for dico in results])

io.sendlineafter(b'>', str(token).encode())
print(io.recvline().decode().strip())