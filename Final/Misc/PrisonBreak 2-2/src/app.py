import time
import pickle
import sys

from jail import Jail

class SafeUnpickler(pickle.Unpickler):
	PICKLE_SAFE = ["jail"]
	def find_class(self, module, name):
		if not module in self.PICKLE_SAFE:
			raise pickle.UnpicklingError('Attempting to unpickle unsafe module %s' % module)
		return super().find_class(module, name)

def whisper(bytescodes):
	open('/tmp/payload.txt', 'wb').write(bytescodes)
	try:
		return SafeUnpickler(file=open('/tmp/payload.txt', 'rb')).load()
	except Exception as ex:
		print(ex)
		pass

def main():
	j = Jail(func=whisper)
	j.run()	

if __name__ == '__main__':
	main()