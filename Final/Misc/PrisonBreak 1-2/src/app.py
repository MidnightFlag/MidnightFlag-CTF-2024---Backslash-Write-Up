import time
import pickle
import yaml
import sys

class SafeUnpickler(pickle.Unpickler):
	PICKLE_SAFE = {'yaml': dir(yaml)}
	def find_class(self, module, name):
		if not module in self.PICKLE_SAFE:
			raise pickle.UnpicklingError('Attempting to unpickle unsafe module %s' % module)
		__import__(module)
		mod = sys.modules[module]
		if not name in self.PICKLE_SAFE[module]:
			raise pickle.UnpicklingError('Attempting to unpickle unsafe class %s' % name)
		klass = getattr(mod, name)
		return klass


def MySafeload(bytescodes):
	open('/tmp/payload.txt', 'wb').write(bytescodes)
	try:
		return SafeUnpickler(file=open('/tmp/payload.txt', 'rb')).load()
	except Exception as ex:
		print(ex)
		pass

def call_guardian():
	inp = input('What is there ?\n')

	try:
		bc = bytes.fromhex(inp)
		MySafeload(bc)
		print("I don't care .")
	except Exception as ex:
		print(ex)
		pass

def menu():
	print('''
================================
 ||     ||<(.)>||<(.)>||     || 
 ||    _||     ||     ||_    || 
 ||   (__D     ||     C__)   || 
 ||   (__D     ||     C__)   ||
 ||   (__D     ||     C__)   ||
 ||   (__D     ||     C__)   ||
 ||     ||     ||     ||     ||
================================  1/2

You're in jail now !

1) Call a guardian
2) Wait
''')

def choice():	
	c = ''
	while not c.isdigit() and c not in ['1', '2']:
		c = input('> ')
	return int(c)

def main():
	menu()
	for _ in range(5):
		c = choice()
		try:
			if c == 1:
				call_guardian()
			else:
				time.sleep(1)
		except Exception as ex:
			print(ex)
			print("An error occured !")

if __name__ == '__main__':
	main()

	