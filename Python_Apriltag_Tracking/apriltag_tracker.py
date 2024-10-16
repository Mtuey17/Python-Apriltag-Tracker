'''
Matthew Tuer-2024

made with the help of this website:
https://pyimagesearch.com/2020/11/02/apriltag-with-python/

focal length calculated with code from here:
https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
'''
import cv2
import apriltag
import math

KNOWN_TAG_WIDTH=6.5

#calculate using link above
FOCAL_LENGTH=1025.341496394231


def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth
 


#---------------MAIN-----------------------------------


device_number=2 #change to your camera number
cap= cv2.VideoCapture(device_number,cv2.CAP_V4L2)

#forcing video format and frame rate 
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FPS, 30)

#set your resolution here
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 820)

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)


while cap.isOpened():

	ret, image = cap.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	results = detector.detect(gray)
	count=0

	for r in results:
		count+=1
		tag_id=r.tag_id
	
		(ptA, ptB, ptC, ptD) = r.corners
		ptB = (int(ptB[0]), int(ptB[1]))
		ptC = (int(ptC[0]), int(ptC[1]))
		ptD = (int(ptD[0]), int(ptD[1]))
		ptA = (int(ptA[0]), int(ptA[1]))
		
		# draw the bounding box of the AprilTag detection
		cv2.line(image, ptA, ptB, (0, 255, 0), 2)
		cv2.line(image, ptB, ptC, (0, 255, 0), 2)
		cv2.line(image, ptC, ptD, (0, 255, 0), 2)
		cv2.line(image, ptD, ptA, (0, 255, 0), 2)
		
		# draw the center (x, y)-coordinates of the AprilTag
		(cX, cY) = (int(r.center[0]), int(r.center[1]))
		cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
		# draw the tag family, ID, and number on the screen
		tagFamily = r.tag_family.decode("utf-8")
		cv2.putText(image, tagFamily + " tag#"+str(count) + " id:"+str(tag_id), (ptA[0], ptA[1] - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		

        #calculating width of highlighted tag to find distance 
		width = math.sqrt((ptB[0] - ptA[0])**2 + (ptB[1] - ptA[1])**2)
		inches = distance_to_camera(KNOWN_TAG_WIDTH, FOCAL_LENGTH, width)

		#displaying distance of tag #1 on video feed 
		if count==1:
			cv2.putText(image, " tag#1:%.2fft" % (inches / 12),
			(image.shape[1] - 240, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
			1.0, (0, 255, 0), 3)
	
		print("tag #%s --center x: %s center y: %s distance: %s" %(count,cX,cY,inches))
		
	if count ==0:
		print("no tags detected...")
	count=0
	cv2.imshow("Image", image)
	cv2.waitKey(1)
	