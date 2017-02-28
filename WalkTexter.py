from bluetoothConnect import *
from sensor import *

# ultrasonic sensor setup
sensor = sensor()

# camera setup

#bluetooth setup
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

bltSoc = bluetoothConnect(client_sock, server_sock)

if __name__ == '__main__':
	try :
		while True:
			# print "hello"
			if sensor.detectObst():
				status = "status:warning"
				bltSoc.send(status)
				time.sleep(1)
			# prepare the string to send
			# data = ******
			# bltSoc.send(data)  

	except (IOError) as err:
		pass

	except (KeyboardInterrupt):
		print "disconnected"
		bltSoc.close()
		print "all done"
	finally:
		sensor.close()