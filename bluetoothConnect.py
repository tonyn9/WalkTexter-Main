from bluetooth import *

class bluetoothConnect:
	def __init__(self):
		server_sock=BluetoothSocket( RFCOMM )
		server_sock.bind(("",PORT_ANY))
		server_sock.listen(1)

		port = server_sock.getsockname()[1]

		uuid = "00001101-0000-1000-8000-00805F9B34FB"

		advertise_service( server_sock, "WalkText",
		                   service_id = uuid,
		                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
		                   profiles = [ SERIAL_PORT_PROFILE ], 
		        		)

		print "Waiting for connection on RFCOMM channel %d" % port
		client_sock, client_info = server_sock.accept()
		print "Accepted connection from " , client_info

		data = client_sock.recv(1024)
		print "received [%s]" % data

		self.client = client_sock;
		self.server = server_sock;

	def recv(self):
		return self.client_sock.recv(1024)

	def send(self, sendMsg):
		self.client_sock.send(sendMsg)
	
	def close(self):
		self.client_sock.close()
		self.server_sock.close()