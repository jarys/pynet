from client import Client
from threading import Thread
import pickle
from test import Test
import time

class ClientSide(Client):
	def __init__(self, name):
		self.looping = False
		self.name = name

	def start(self):
		self.connect('192.168.1.14', 64444)
		print('client connected')
		Thread(target=self.loop).start()

	def stop(self):
		self.looping = False
		self.quit()

	def loop(self):
		self.looping = True
		while self.looping:
			self.send(b'hey?' + self.name)
			response = self.recv()
			di, data = response[:4], response[4:] #di = id
			if di == b'yes!':
				Thread(target=self.keep_deamon).start()
				opened_test = pickle.loads(data)
				opened_test.start()
				finished_test = pickle.dumps(opened_test)
				self.deamon = False
				self.send(b'end!' + finished_test)
			elif di == b'no! ':
				pass
			else:
				print('[CLIENT]: invalid response:', response)

			time.sleep(5)

	def keep_deamon(self):
		time.sleep(2.5)
		self.deamon = True
		while self.deamon:
			self.send(b'keep ' + self.name + b' alive')
			time.sleep(10)





if __name__ == '__main__':

	name = ''
	while not name:
		print('1=win7 | 2=win10 | 3=suse')
		machine = input('Choose machine: ')

		if machine == '1':
			name = b'win7 '

		elif machine == '2':
			name = b'win10'

		elif machine == '3':
			name = b'suse '

	import sys #print into file

	if sys.argv[1:] == ['-s']:
		print('silent mode on')
		sys.stdout = open('log-cli.txt', 'w')

	c = ClientSide(name)
	c.start()