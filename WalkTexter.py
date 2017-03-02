from bluetoothConnect import *
from cvDetection import *
from sensor import *

#bit set up
SENSOR_BIT_FLAG = 1

# ultrasonic sensor setup
sensor = sensor()

# CV setup
cvDetection = cvDetection()

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
			bit = 0
			isDetected = False
			findSign = False
			if sensor.detectObst():
				bit ^= SENSOR_BIT_FLAG
				isDetected = True
			findSign, detectedBitFlag = cvDetection.isCVDetected()
			if findSign:
				bit ^= detectedBitFlag
				isDetected = True
			if isDetected:
				print bin(bit)
				status = "status:warning:" + str(bit)
				bltSoc.send(status)
				time.sleep(2)

	except (IOError) as err:
		pass

	except (KeyboardInterrupt):
		print "disconnected"
		bltSoc.close()
		print "all done"
	finally:
		sensor.close()
