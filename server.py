import socketserver
import json
from queue import Queue
import time

clients = set ()
queue_of_clients = Queue ()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class RouterTCPServer (socketserver.StreamRequestHandler):
	def _recvall (self):
		BUFF_SIZE = 1
		data = b""
		while True:
			part = self.request.recv (BUFF_SIZE)
			data += part
			if part == b'\n':
				break
			if len(part) < BUFF_SIZE:
				break
		return str(data, 'utf-8').strip ()

	def setup (self):
		print('{}:{} connected'.format(*self.client_address))
		clients.add (self.request)
		print ('Clients:', len(clients))

	def finish (self):
		print('{}:{} disconnected'.format(*self.client_address))
		clients.remove (self.request)
		print ('Clients:', len(clients))

	def handle (self):
		while True:
			self.data = self._recvall ()
			print ('{} wrote: '.format (self.client_address), end='')
			print (self.data)

			self.data = json.loads (self.data)	

			print (self.data)
	
			if 'error' in self.data:
				self.request.sendall (bytes ('Error: Data = { ' + json.dumps (self.data) + ' } is not valid\n', 'utf-8'))

			elif not 'status' in self.data:
				self.request.sendall (bytes ('Error: Data = { ' + json.dumps (self.data) + ' } is not valid\n', 'utf-8'))

			elif self.data ['status'] == 0: # free
				queue_of_clients.put (self.request)
				self.request.sendall (bytes ('wait\n', 'utf-8'))

			# received task partial results or full results
			elif self.data ['status'] == 1: # busy
				if self.data ['progress']['ready'] == self.data ['progress']['total']:
					# TODO: update score in db...
					self.request.sendall (bytes ('wait\n', 'utf-8'))
				elif self.data ['progress']['ready'] != self.data ['progress']['total']:
					# TODO: update testing status in db...
					self.request.sendall (bytes ('wait\n', 'utf-8'))

from threading import Thread

def checkDB (socketServer):
	print (socketServer)
	print (dir(socketServer))
	print (dir(socketServer.socket))
	while True:
		task = {'name': 'shit'} # TODO: get task from DB
		#print ('Queue:', queue_of_clients.qsize ())
		#print ('Clients:', len(clients))
		while queue_of_clients.empty (): continue # wait 'till some client become free
		#print ('Queue:', queue_of_clients.qsize ())
		#print ('Clients:', len(clients))
		try:
			free_client = queue_of_clients.get ()
		except:
			print ('Error: cannot get from queue')
			continue
		try:
			free_client.sendall (bytes ('task\n', 'utf-8'))
		except:
			print ('Error: cannot send "task" to', free_client)
			continue
		try:
			free_client.sendall (bytes (json.dumps (task) + '\n', 'utf-8'))
		except:
			print ('Error: cannot send the task to', free_client)
			continue

if __name__ == '__main__':
	HOST, PORT = 'localhost', 8000

	with ThreadedTCPServer ((HOST, PORT), RouterTCPServer) as server:
		t = Thread (target=checkDB, args=(server,))
		t.start ()
		
		server.serve_forever ()
