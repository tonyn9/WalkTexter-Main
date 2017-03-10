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
from joblib import Parallel, delayed
import multiprocessing

# defining and init vars
IMAGE_SIZE = 200.0
#MATCH_THRESHOLD = 3
FRAME_THRESHOLD = 10
NUM_DETECTED_THRESHOLD = 3
#STOPSIGN_BIT_FLAG = 2

cascadeNameList = ['frontal_stop_sign_cascade.xml','dont_walk_cascade.xml', 'walk_cascade.xml']
prototypeNameList = ['stopPrototype.png','dontWalkPrototype.png','walkPrototype.png']
matchThresHoldList = [3,160,150]
minNeighborsList = [3,6,6]

class cvDetectionClass:
	#stopSignCascade = None
	cascadeList = []
	prototypeList = []
	cap = None
	#stopSignPrototype = None
	def __init__(self):
		#self.stopSignCascade = cv2.CascadeClassifier('frontal_stop_sign_cascade.xml')
		#self.stopSignPrototype = cv2.imread('stopPrototype.png',0)
		for cascade, prototype in zip(cascadeNameList,prototypeNameList):
			self.cascadeList.append(cv2.CascadeClassifier(cascade))
			self.prototypeList.append(cv2.imread(prototype,0))

		self.cap = cv2.VideoCapture(0)
		if not self.cap.isOpened():
			if __debug__:
				print "DEBUG: camera can not be opened"
			exit()
		time.sleep(0.1)

	def isCVDetected(self):
		bit = 0
		returnFlag = False
		# numOfDetected = 0

		# for i in range(FRAME_THRESHOLD):
		ret, frame = self.cap.read()

		# num_cores = multiprocessing.cpu_count()

		#bitResult = Parallel(n_jobs=1)(delayed(self.isThisCascadeDetected)(frame, self.cascadeList[i], self.prototypeList[i], matchThresHoldList[i], minNeighborsList[i]) for i in range(len(self.cascadeList)))
		
		for i in range(len(self.cascadeList)):
			if self.isThisCascadeDetected(frame, self.cascadeList[i], 
					self.prototypeList[i], matchThresHoldList[i], minNeighborsList[i]):   
				returnFlag = True
				bit ^= 2**(i+1)

				# numOfDetected += 1
				# if numOfDetected > NUM_DETECTED_THRESHOLD:
				# 	bit ^= 2**(i+1)
				# 	return True, bit

		# for i in range(len(numOfDetected)):
		# 	if bitResult[i]:
		# 		numOfDetected[i] += 1

		# for i in range(len(numOfDetected)):
		# 	if numDetected[i] >= NUM_DETECTED_THRESHOLD:
		# 		bit ^= 2**(i+1)
		# 		returnFlag = True
		
		return returnFlag, bit
		

	def isThisCascadeDetected(self, frame, xml, prototype, matchThreshold, minNeighbor):  
		gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		haarCascadeObject = xml.detectMultiScale(
								gray, 
								scaleFactor=1.4, 
								minNeighbors=minNeighbor)

		orb = cv2.ORB_create()
		bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
		kp_r,des_r = orb.detectAndCompute(prototype,None)

		isFoundMatch = False

		for (x,y,w,h) in haarCascadeObject:

			# obtain object from street image
			obj = gray[y:y+h,x:x+w]
			ratio = IMAGE_SIZE / obj.shape[1]
			obj = cv2.resize(obj,(int(IMAGE_SIZE),int(obj.shape[0]*ratio)))

			# find the keypoints and descriptors for object
			kp_o, des_o = orb.detectAndCompute(obj,None)
			if len(kp_o) == 0 or des_o is None: continue

			# match descriptors
			matches = bf.match(des_r,des_o)

			# draw object on street image, if threshold met
			if(len(matches) >= matchThreshold):
				if __debug__:
					print "DEBUG: Found a match! Length of match: %d" % len(matches)
				isFoundMatch = True

		return isFoundMatch

	def close(self):
		self.cap.release()
		cv2.destroyAllWindows()

	def processInput(self, i):
		return i * i

	
