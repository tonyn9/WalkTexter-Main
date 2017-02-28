from bluetooth import *

class bluetoothConnect:
	client = None
	server = None
	def __init__(self, client_sock, server_sock):
		self.client = client_sock
		self.server = server_sock

		while True:
			data = client_sock.recv(1024)
			if len(data) != 0:
				print "received [%s]" % data
				break
		print "break the loop"


	def recv(self):
		return self.client.recv(1024)

	def send(self, sendMsg):
		self.client.send(sendMsg)
	
	def close(self):
		self.client.close()
		self.server.close()