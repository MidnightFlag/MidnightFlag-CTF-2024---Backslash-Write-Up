import time

class Jail:
	def __init__(self, func):
		self.whisper = func

	def call_guardian(self):
		inp = input('What is there ?\n')
		try:
			bc = bytes.fromhex(inp)
			self.whisper(bc)
			print("I don't care .")
		except Exception as ex:
			print(ex)
			pass

	def menu(self):
		print('''
================================
 ||     ||<(.)>||<(.)>||     || 
 ||    _||     ||     ||_    || 
 ||   (__D     ||     C__)   || 
 ||   (__D     ||     C__)   ||
 ||   (__D     ||     C__)   ||
 ||   (__D     ||     C__)   ||
 ||     ||     ||     ||     ||
================================  2/2

You're in jail now !

1) Call a guardian
2) Wait
''')

	def choice(self):	
		c = ''
		while not c.isdigit() and c not in ['1', '2']:
			c = input('> ')
		return int(c)

	def run(self):
		for _ in range(5):
			c = self.choice()
			try:
				if c == 1:
					self.call_guardian()
				else:
					time.sleep(1)
			except Exception as ex:
				print(ex)
				print("An error occured !")
