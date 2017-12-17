import socket
import sys
import json
import time

class client:
	WAITING, BUSY = range (2)
	
	def __init__ (self, socketLogs, HostPort):
		self.status = self.WAITING
		self.progress = {}
		self.interface, self.socketAction = socketLogs
		self.host, self.port = HostPort
		self.socketToServer = None
		self.init_socket ()

	def _recvall (self, sock):
		BUFF_SIZE = 1
		data = b""
		while True:
			part = sock.recv (BUFF_SIZE)
			data += part
			if part == b'\n':
				break
			if len(part) < BUFF_SIZE:
				break
		return str(data, 'utf-8').strip ()

	def init_socket (self):
		if self.socketToServer == None:
			self.socketToServer = socket.socket (self.interface, self.socketAction)
			self.socketToServer.connect ((self.host, self.port))
			self.send_stats ()

	def send_stats (self):
		self.init_socket ()
		self.socketToServer.sendall (bytes (json.dumps ({'status': self.status, 'progress': self.progress}) + '\n', 'utf-8'))
	
	def eval_task (self):
		self.init_socket ()
		received = self._recvall (self.socketToServer) # get task
		#time.sleep (0.4)
		
		self.status = self.BUSY
		self.progress = {'ready': 5, 'total': 20, 'points': float('nan')}
		self.send_stats ()
		
		self.progress = {'ready': 20, 'total': 20, 'points': 0.95}
		self.send_stats ()

		self.status = self.WAITING
		self.progress = {}
		self.send_stats ()

	def ping (self):
		self.init_socket ()
		received = self._recvall (self.socketToServer) # get task
		#time.sleep (0.4)

		if received == 'ping':
			self.send_stats ()
		elif received == 'task':
			self.eval_task ()
		elif received == 'wait':
			print ('waiting')
			pass
		elif received == '':
			#print ('connection finished')
			self.socketToServer = None
			pass
		else:
			print ('Received: "', received, '"')
			print ('Error: invalid ping -', received)
			#self.socketToServer.sendall (bytes (json.dumps ({'error': 'invalid ping', 'type': received}), 'utf-8'))
			pass


sample_client = client((socket.AF_INET, socket.SOCK_STREAM), ('localhost', 8000))

while True:
	sample_client.ping ()
	
