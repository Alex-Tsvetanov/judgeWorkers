import socketserver
import json
import asyncio

clients = set ()
queue_of_clients = asyncio.Queue ()

class RouterTCPServer (socketserver.StreamRequestHandler):
	def _recvall (self):
		BUFF_SIZE = 4096
		data = b""
		while True:
			part = self.request.recv (BUFF_SIZE)
			data += part
			if len(part) < BUFF_SIZE:
				break
		return str(data, 'utf-8')

	def setup (self):
		print('{}:{} connected'.format(*self.client_address))
		clients.add (self.client_address)
		print ('Clients:', len(clients))

	def finish (self):
		print('{}:{} disconnected'.format(*self.client_address))
		clients.remove (self.client_address)
		print ('Clients:', len(clients))

	def handle (self):
		while True:
			self.data = self._recvall ()
			print ('{} wrote: '.format (self.client_address), end='')
			print (self.data)

			self.data = json.loads (self.data)	

			print (self.data)

			if self.data ['status'] == 0: # free
				global queue_of_clients # this line does NOT change the situation
				print ('new element to queue', queue_of_clients.qsize ()) # 0
				print ('new element to queue', queue_of_clients.empty ()) # True
				print ('new element to queue', self.client_address) # Any address
				queue_of_clients.put (self.client_address)
				print ('new element to queue', queue_of_clients.qsize ()) # Here we can see size of the queue is unchanged
				print ('new element to queue', queue_of_clients.empty ()) # and it is continuing to be empty, but clients is changed?!?!
				self.request.sendall (bytes ('wait', 'utf-8'))

			# received task partial results or full results
			elif self.data ['status'] == 1: # busy
				if self.data ['progress']['ready'] == self.data ['progress']['total']:
					# update score in db...
					self.request.sendall (bytes ('wait', 'utf-8'))
				elif self.data ['progress']['ready'] != self.data ['progress']['total']:
					# update testing status in db...
					self.request.sendall (bytes ('wait', 'utf-8'))
			else:	
				self.request.sendall (bytes ('Error: Data = { ' + json.dumps (self.data) + ' } is not valid', 'utf-8'))

from threading import Thread

def checkDB (socketServer):
	while True:
		task = {'name': 'shit'}
		print (queue_of_clients.qsize ())
		print ('Clients:', len(clients))
		while True:
			try:
				free_client = queue_of_clients.get ()
				socketServer.sendto (bytes (json.dumps (task), 'utf-8'), free_client)
			except:
				continue

if __name__ == '__main__':
	HOST, PORT = 'localhost', 8000

	with socketserver.TCPServer ((HOST, PORT), RouterTCPServer) as server:
		t = Thread (target=checkDB, args=(server,))
		t.start ()
		server.serve_forever ()
