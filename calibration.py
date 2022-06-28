#imports
from scipy.spatial.distance import cdist
import numpy as np
import imutils
from imutils import contours
from imutils import perspective
import cv2



filename = 'media/video.mp4'
pixels_per_cm = 0



#-----AUTOMATIC CALIBRATION USING ARUCO MARKER-----#
#code largely taken from https://arshren.medium.com/measure-object-size-using-opencv-and-aruco-marker-fa8b2e3b0572

def findArucoMarker(image, markerSize=5, totalMarkers=100, draw=True):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	key = getattr(cv2.aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')

	arucoDict = cv2.aruco.Dictionary_get(key)

	arucoParam = cv2.aruco.DetectorParameters_create()

	bboxs, idx, rejected = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

	return bboxs, idx, rejected


def automaticallyCalibrate():

	global pixels_per_cm

	# dimensions of aruco printout are 7x7 cm so perimeter is 7*4 cm
	true_aruco_perimeter = 7 * 4

	cap = cv2.VideoCapture(filename)
	ret, image = cap.read()

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7,7), 0)

	edged = cv2.Canny(gray, 50, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	(cnts, _) = contours.sort_contours(cnts)

	arucofound = findArucoMarker(image, totalMarkers=100)
		
	vertices = []

	for i in range(4):
		point = []
		curr_x = arucofound[0][0][0][i][0]
		curr_y = arucofound[0][0][0][i][1]
		point.append(curr_x)
		point.append(curr_y)
		vertices.append(point)

	vertices = np.asarray(vertices, dtype=np.int32)
	np_pts = vertices.reshape((-1,1,2))
	cv2.polylines(image, [np_pts], isClosed=True, color=(255,255,0), thickness=5)

	if len(arucofound[0])!=0:
		virtual_aruco_perimeter = cv2.arcLength(arucofound[0][0][0], True)
		print("marker perimeter: {} pixels".format(virtual_aruco_perimeter))
		pixels_per_cm  = virtual_aruco_perimeter / true_aruco_perimeter
		print("{} pixels per cm".format(pixels_per_cm))
		return 1
	else:
		print("Automatic calibration failed")
		return 0





#-----MANUAL CALIBRATION-----#

all_points = []
cap = cv2.VideoCapture(filename)
ret, image = cap.read()

def selectPoints(event, x, y, flags, param):
	global all_points
	point = []
	if event == cv2.EVENT_LBUTTONDOWN:
		point.append(x)
		point.append(y)
		all_points.append(point)
		cv2.circle(image, (x,y), 10, (0,255,0), 10)


#calculates the average distance between each consecutive pair of labeled points 
def getAvgDist(all_points):
	all_dists = []
	num_points = len(all_points)
	for i in range(num_points-1):
		p_1 = np.array(all_points[i])
		p_2 = np.array(all_points[i+1])
		dist = np.linalg.norm(p_1 - p_2)	
		all_dists.append(dist)
	avg_distance = np.sum(all_dists) / (num_points - 1)
	return avg_distance


def manuallyCalibrate():
	global pixels_per_cm
	cv2.namedWindow(winname='calibration')
	cv2.setMouseCallback('calibration', selectPoints)
	while True:
		cv2.imshow('calibration', image)
		if cv2.waitKey(1) & 0xFF == 27:
			break
	pixels_per_cm = getAvgDist(all_points)
	cv2.destroyAllWindows()







#-----MAIN DRIVER-----#
def calibrate():
	try:
		automaticallyCalibrate()
	except:
		print("Automatic calibration failed")
		print("Opening manual calibration")
		manuallyCalibrate()
	print("CALIBRATION COMPLETE: {} pixels per cm.".format(pixels_per_cm))


calibrate()
