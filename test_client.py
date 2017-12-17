import socket
import sys

HOST, PORT = 'localhost', 8000
data = ' '.join (sys.argv [1:])

def recvall (sock):
	BUFF_SIZE = 4096
	data = b""
	while True:
		part = sock.recv (BUFF_SIZE)
		data += part
		if len(part) < BUFF_SIZE:
			break
	return str(data, 'utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.connect ((HOST, PORT))
	sock.sendall (bytes (data + '\n', 'utf-8'))

	received = recvall (sock)

print ('Sent:     {}'.format (data))
print ('Received: {}'.format (received))
