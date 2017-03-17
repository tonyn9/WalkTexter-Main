###############################################################
## Copyright TEAM SALT 2017 - All Rights Reserved 
## 
## File: WalkTexter.py
##
## Description:
##		Main program for Walk Texter running on raspberry pi
##
## History:
##		Date		Update Description		Developer
##	------------	-------------------		------------
##	2/27/2017		Created					SC,AY
##
###############################################################

# import user-defined classes
from bluetoothConnect import *
from cvDetection import *
from sensor import *


# defining vars
SENSOR_BIT_FLAG = 1		#big flag indicating that sensor has detected an obstacle
THRESHOLD = 2

# ultrasonic sensor setup
sensor = sensorClass()	#creating a sensor class

# CV setup
cvDetect = cvDetectionClass()   #creating a cvDetection class

# bluetooth setup
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805F9B34FB"

advertise_service( server_sock, "WalkText",
					service_id = uuid,
					service_classes = [ uuid, SERIAL_PORT_CLASS ],
					profiles = [ SERIAL_PORT_PROFILE ] )

if __debug__:
	print "Waiting for connection on RFCOMM channel %d" % port
client_sock, client_info = server_sock.accept()
if __debug__:
	print "Accepted connection from " , client_info

bltSoc = bluetoothConnectClass(client_sock, server_sock)   #create a bluetoothConnect class

if __name__ == '__main__':
	try :

		# init the frame filter
		bitArray = [0,0,0] #stopSign, dontWalk, Walk
		numOfFrame = 0

		while True:

			# init and set some local vars
			detectBitsMsg = 0	#this var will be send to the android app if something has been detected
								#each bit position determines if a certan detection has been detected
			
			isDetected = False	#flag is init to false, set to true if something has been detected to send it
			cvHasFoundSign = False 	#flag is init to false, set to true if CVdetect has detected something
			isSensorDetected = False
			# ultrasonic sensor processing
			if sensor.detectObst():
				detectBitsMsg ^= SENSOR_BIT_FLAG 	#set the first bit to 1
				isDetected = True 	#set detection flag to true to send it to app
				isSensorDetected = True
			# image processing
			if not isDetected:
				# check if cvDetection has detected something
				cvHasFoundSign, detectedBitFlag = cvDetect.isCVDetected()
				numOfFrame += 1
				if cvHasFoundSign: 	#if cvDetection found something
 					for i in range(3):

 						# determine which match was found 
						bitArray[i] += (detectedBitFlag & (2**(i+1))) >> (i+1)
						if bitArray[i] >= THRESHOLD:
							detectBitsMsg ^= 2**(i+1)
							bitArray[i] = 0
							isDetected = True

				# reset frames
				if numOfFrame >= 10:
					numOfFrame = 0;

					# reset frame bits
					for i in range(3):
						bitArray[i] = 0

			# prepare and send message to the phone
			if isDetected:
				if __debug__:
					print bin(detectBitsMsg)
				status = "status:warning:" + str(detectBitsMsg)
				bltSoc.send(status)
				
				# sleeping for 2 sec if sensor was detected
				if isSensorDetected:
					time.sleep(1)

	except (IOError) as err:
		pass

	except (KeyboardInterrupt):
		if __debug__:
			print "disconnected"

		# close/cleanup bluetooth and cvdetection
		bltSoc.close()
		cvDetect.close()
		if __debug__:
			print "all done"
	finally:
		sensor.close()
