###############################################################
## Copyright TEAM SALT 2017 - All Rights Reserved 
## 
## File: sensor.py
##
## Description:
##		sensor class
##
## History:
##		Date		Update Description		Developer
##	------------	-------------------		------------
##	2/27/2017		Created					SC,AY
##
###############################################################

# importing libraries
import time
import RPi.GPIO as GPIO

# GPIO pins (using BCM)
TRIG = 23
ECHO = 24

# defining and init vars
DISTANCE_THRESHOLD = 150

class sensorClass:
	def __init__(self):
		if not __debug__:
			GPIO.setwarnings(False)
		
		# setup GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(TRIG,GPIO.OUT)
		GPIO.setup(ECHO,GPIO.IN)

		GPIO.output(TRIG, False)
		
		time.sleep(2) #sleep for 2 sec to let the sensor settle
	
	# detectObstacle method
	def detectObst(self):
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		# send an echo and time the time it takes for it to come back
		while GPIO.input(ECHO) == 0:
			pulse_start = time.time()

		while GPIO.input(ECHO) == 1:
			pulse_end = time.time()

		# calculate the distance
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)

		if __debug__ and 7 < distance < DISTANCE_THRESHOLD:
			print 'distance=' + str(distance)

		# return if the distance is less than the threshold
                if 9 < distance < DISTANCE_THRESHOLD:
                        return True
                return False
	# close/cleanup method
	def close(self):
		GPIO.cleanup()
