###############################################################
## Copyright TEAM SALT 2017 - All Rights Reserved 
## 
## File: cvDetection.py
##
## Description:
##		cvDetection class
##
## History:
##		Date		Update Description		Developer
##	------------	-------------------		------------
##	2/27/2017		Created					SC,AY
##
###############################################################

# include libraries
import time
import cv2

# defining and init vars
IMAGE_SIZE = 200.0

# list of cascade name, prototype name, match threhold, and min neighbor
cascadeNameList = ['frontal_stop_sign_cascade.xml','dont_walk_cascade.xml', 'walk_cascade.xml']
prototypeNameList = ['stopPrototype.png','dontWalkPrototype.png','walkPrototype.png']
matchThresHoldList = [3,160,150]
minNeighborsList = [3,6,6]

class cvDetectionClass:
	cascadeList = []
	prototypeList = []
	cap = None

	def __init__(self):

		# load all the cascade classifiers and the prototype images 
		for cascade, prototype in zip(cascadeNameList,prototypeNameList):
			self.cascadeList.append(cv2.CascadeClassifier(cascade))
			self.prototypeList.append(cv2.imread(prototype,0))

		# turn on the video camera
		self.cap = cv2.VideoCapture(0)
		if not self.cap.isOpened():
			if __debug__:
				print "DEBUG: camera can not be opened"
			exit()
		time.sleep(0.1) 	# let the camera settle down 


	def isCVDetected(self):

		# bit indicates which type of object has been detected by setting the corresponding bit position to 1
		bit = 0

		# return flag initially set to 0 indicating that no match has been found
		returnFlag = False
	
		# read one frame
		ret, frame = self.cap.read()
		
		# loop through each different element in the cascade list and check if the object is matched on the frame
		for i in range(len(self.cascadeList)):
			if self.isThisCascadeDetected(frame, self.cascadeList[i], 
					self.prototypeList[i], matchThresHoldList[i], minNeighborsList[i]):   
				
				# if found, set the returnFlag to true and the bit position of the correponding to 1
				returnFlag = True
				bit ^= 2**(i+1)

		return returnFlag, bit
		

	def isThisCascadeDetected(self, frame, xml, prototype, matchThreshold, minNeighbor):  
		
		# init found match to false
		isFoundMatch = False

		# perform the haar cascade detection
		gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		haarCascadeObject = xml.detectMultiScale(
								gray, 
								scaleFactor=1.4, 
								minNeighbors=minNeighbor)

		# init ORB and BFMatcher which is an additional filtering
		orb = cv2.ORB_create()
		bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
		kp_r,des_r = orb.detectAndCompute(prototype,None)

		# for each object that was found with haarcascade, perform ORB and BFMatcher to try to filter out false alarms
		for (x,y,w,h) in haarCascadeObject:

			# locate the object in the frame
			obj = gray[y:y+h,x:x+w]

			# convert the same ratio as the prototype image
			ratio = IMAGE_SIZE / obj.shape[1]
			obj = cv2.resize(obj,(int(IMAGE_SIZE),int(obj.shape[0]*ratio)))

			# ORB
			kp_o, des_o = orb.detectAndCompute(obj,None)
			if len(kp_o) == 0 or des_o is None: continue

			# BFMatcher
			matches = bf.match(des_r,des_o)

			# if the matches is greater than the match threshold, most likely their is a good match
			if(len(matches) >= matchThreshold):
				if __debug__:
					print "DEBUG: Found a match! Length of match: %d" % len(matches)
				isFoundMatch = True

		return isFoundMatch

	def close(self):
		self.cap.release()
		cv2.destroyAllWindows()
