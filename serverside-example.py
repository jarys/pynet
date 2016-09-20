import time
import socket
import protocol
from server import Server
import pickle
import threading
from timeit import default_timer as timer

from datetime import datetime

class ServerSide(Server):
	def __init__(self):
		self.opened_tests = {'win7':  [],
							 'win10': [], 
							 'suse':  []}
		self.active_machine = None
		self.last_keep_me = 0
		self.print_time = 0

	def handle_data(self, data):
		print('[SERVER]: data =', data if len(data) < 20 else (data[:20] + b'...'))
		#PING-PONG
		if data == b'ping':
			self.send_data(b'pong')
			return
		#ID
		di, data = data[:4], data[4:] #di = id
		#TEST TO RUN
		if di == b'hey?':
			if self.active_machine and timer() - self.last_keep_me > 120:
				print('[SERVER]: {} timeout'.format(self.active_machine))
				self.remove_socket(self.sending_socket)
				self.active_machine = None

			if self.active_machine:
				self.send_data(b'no! net')
				return
			name = data[:5].decode('utf-8').strip()

			if not name in self.opened_tests.keys():
				self.send_data(b'no! name ' + name.encode() + '.')
				return

			if self.opened_tests[name]:
				self.active_machine = name
				self.last_keep_me = timer()
				test = self.opened_tests[self.active_machine][0]
				test = pickle.dumps(test)
				self.send_data(b'yes!' + test)
			else:
				self.send_data(b'no! tests')
		#TEST FINISHED
		elif di == b'end!':
			test = pickle.loads(data)
			with open(test.filename, 'wb') as file:
				file.write(data)
			self.opened_tests[self.active_machine].pop(0)
			self.active_machine = None
		#NEW TEST
		elif di == b'new?':
			try:
				name, data = data[:5].decode('utf-8').strip(), data[5:]
				test = pickle.loads(data)
				self.insert_test(test, self.opened_tests[name])
				self.send_data(b'acce')
			except:
				print('[SERVER]: Error in reception.')
				self.send_data(b'refu')
		elif di == b'keep':
			self.last_keep_me = timer()
		elif di == b'info':
			print(data.decode('utf-8'))
		elif di == b'exec':
			exec(data.decode('utf-8'))
		else:
			print('[SERVER]: Rubbish:', di + data)


		if self.print_time == 0:
			print('[SERVER]: time =', datetime.now())
			self.print_time = 10
		else:
			self.print_time -= 1

	def insert_test(self, test, queue):
		if not queue:
			queue.append(test)
			return

		for i, t in enumerate(queue):
			if test.priority > t.priority:
				queue.insert(i, test)
				break
		else:
			queue.append(test)

	def loop(self):
		threading.Thread(target=self.serve_forever).start()






if __name__ == '__main__':
	import sys #print into file
	if sys.argv[1:] == ['-s']:
		print('silent mode on')
		sys.stdout = open('log-srv.txt', 'w')
		
	s = ServerSide()
	s.connect('192.168.1.14', 64444)
	s.loop()
