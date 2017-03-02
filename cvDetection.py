import time
import cv2

IMAGE_SIZE = 200.0
MATCH_THRESHOLD = 3
FRAME_THRESHOLD = 10
NUM_DETECTED_THRESHOLD = 3
STOPSIGN_BIT_FLAG = 2
class cvDetection:
	stopSignCascade = None
	cap = None
	stopSignPrototype = None
	def __init__(self):
		self.stopSignCascade = cv2.CascadeClassifier('frontal_stop_sign_cascade.xml')
		self.stopSignPrototype = cv2.imread('stopPrototype.png',0)
		self.cap = cv2.VideoCapture(0)
		if not self.cap.isOpened():
			print "DEBUG: camera can not be opened"
			exit()
		time.sleep(0.1)

	def isCVDetected(self):
		bit = 0
		numOfDetected = 0
		for i in range(FRAME_THRESHOLD):
			ret, frame = self.cap.read()
			if self.isThisCascadeDetected(frame, self.stopSignCascade, self.stopSignPrototype):   
				numOfDetected += 1
				if numOfDetected > NUM_DETECTED_THRESHOLD:
					bit ^= STOPSIGN_BIT_FLAG 
					return True, bit
		return False, bit
		

	def isThisCascadeDetected(self, frame, xml, prototype):  
		gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		haarCascadeObject = xml.detectMultiScale(
								gray, 
								scaleFactor=1.4, 
								minNeighbors=3)

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
			if(len(matches) >= MATCH_THRESHOLD):
				print "DEBUG: Found a match! Length of match: %d" % len(matches)
				isFoundMatch = True

		return isFoundMatch

	def close(self):
		self.cap.release()
		cv2.destroyAllWindows()