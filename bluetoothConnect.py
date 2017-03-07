###############################################################
## Copyright TEAM SALT 2017 - All Rights Reserved 
## 
## File: bluetoothConnect.py
##
## Description:
##		blutoothConnect class
##
## History:
##		Date		Update Description		Developer
##	------------	-------------------		------------
##	2/27/2017		Created					SC,AY
##
###############################################################

# import library
from bluetooth import *

class bluetoothConnectClass:
	client = None
	server = None
	def __init__(self, client_sock, server_sock):

		# set the client and server sockets
		self.client = client_sock
		self.server = server_sock

		# first receive a message from the phone app
		while True:
			data = client_sock.recv(1024)
			if len(data) != 0:
				if __debug__:
					print "received [%s]" % data
				break
		if __debug__:
			print "break the loop"

	# receive method
	def recv(self):
		return self.client.recv(1024)

	# send method
	def send(self, sendMsg):
		self.client.send(sendMsg)
	
	# close/cleanup method
	def close(self):
		self.client.close()
		self.server.close()