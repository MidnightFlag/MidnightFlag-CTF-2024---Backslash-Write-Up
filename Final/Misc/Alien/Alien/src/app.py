import random, os
import hashlib
import string
import time
import math

flag = os.getenv('FLAG', 'flag{ThisIsTheFlag}')

def gen_token():
	def gen_word(x):
		return ''.join([random.choice('abcdeghijklmnopqrstuvwxz') for _ in range(x)])
	return ' '.join([ gen_word(random.randint(4,12)) for _ in range(random.randint(3,6)) ])
	

def logo():
	print('''
      _       _
     (_\\     /_)
       ))   ((
     .-"""""""-.
 /^\\/  _.   _.  \\/^
 \\(   /__\\ /__\\   )/
  \\,  \\o_/_\\o_/  ,/
    \\    (_)    /
     `-.'==='.-'
      __) - (__
     /  `~~~`  \\
    /  /     \\  \\
    \\ :       ; /
     \\|==(*)==|/
      :       :
       \\  |  /
     ___)=|=(___
    {____/ \\____}

''')

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

def convert_message(msg):
	return [convert_int(ord(x)) for x in msg]

def slow_print(msg):
	for l in msg:
		print(l, end='', flush=True)
		time.sleep(0.05)
	time.sleep(0.7)

def init():
	messages = [
		'Connection initialization ...\n',
		'Hanshake exchange ...\n',
		'Password verification ...\n',
		'New message pending:\n'
	]
	for m in messages:
		slow_print(m)

def get_input():
	buffer = ''
	print("Now it's your turn to speak:")
	while 1:
		try:
			x = input('> ')
			if any([y not in ')(]([~+-*=' for y in x]):
				return False
			k = chr(eval(x))
			if k == '\n':
				return buffer
			else:
				buffer += k
		except:
			return False

def main():
	logo()
	init()
	token = gen_token()
	[print(x) for x in convert_message('Hello Human, are you friendly ?\n')]
	[print(x) for x in convert_message('I want to make sure you speak my language\n')]
	[print(x) for x in convert_message(f'Can you say "{token}\\n" in less than 3 seconds? \n')]

	guess = get_input()
	
	if token == guess:
		[print(x) for x in convert_message('We can talk now !\n')]
		[print(x) for x in convert_message(f'Here is the flag: {flag}\n')]
	else:
		slow_print('The alien ran away, he didn\'t like your answer!\n')




if __name__ == '__main__':
	main()