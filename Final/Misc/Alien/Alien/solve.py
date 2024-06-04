from pwn import *

context.log_level = 'critical'

def convert_int(n):
	expr2 = '(~(()==()))*(~(()==[]))'
	if n == 2:
		return expr2
	elif n == 1:
		return '(~(()==[]))*(~(()==[]))'
	elif n == 0:
		return f'({convert_int(1)}-{convert_int(1)})'
	exp = int(math.log2(n))
	res = n - 2**exp
	next_ = f'(({expr2})**({convert_int(exp)}))'
	return f'({next_}+{convert_int(res)})' if res else next_

io = remote('13.38.208.179', int(10182))
# io = process(['python3', './src/app.py'])

io.recvuntil(b'pending:')
io.recvline()

buffer = ''

res = io.recvline().strip().decode()
while 'speak:' not in res:
	buffer += chr(eval(res))
	res = io.recvline().strip().decode()

to_say = re.findall(r'Can you say "(.*?)\\n" in less', buffer)[0]

print('Sentence: "%s"' % to_say)

for letter in to_say:
	io.sendlineafter(b'>', convert_int(ord(letter)).encode())

io.sendlineafter(b'>', convert_int(ord('\n')).encode())

res = io.recvline().strip().decode()
while 1:
	print(chr(eval(res)), end='', flush=True)
	res = io.recvline().strip().decode()