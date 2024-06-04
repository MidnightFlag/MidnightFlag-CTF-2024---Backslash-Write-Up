import random, os
import hashlib
import string

flag = os.getenv('FLAG', 'flag{ThisIsTheFlag}')
charset = string.printable[:-5]

def encrypt(letter: bytes, deepth: int=50) -> bytes:
	encrypt = hashlib.sha1(letter.encode()).hexdigest()
	for _ in range(deepth):
		encrypt = hashlib.sha1(encrypt.encode()).hexdigest()
	return encrypt

def fake(deepth: int=5000):
	c = random.choice(charset)
	for _ in range(deepth):
		c = random.choice(charset)
	return c

def main():	
	token = ''.join([random.choice(charset) for _ in range(10)])
	asked = set()

	while 1:
		try:
			index = input('> ')

			if index == token:
				print(f'Well played, here is the flag: {flag}')

			elif index.isdigit():

				if int(index) in asked:
					print('Who do you think I am? ')
					exit()
				else:
					asked.add(int(index))

				if random.randint(0, 1):
					print(encrypt(token[int(index)]))
				else:
					print(encrypt(fake()))
			else:
				print('You should enter index or the token !')

		except Exception as ex:
			print(ex)
			print('An error occured  ..')


if __name__ == '__main__':
	main()