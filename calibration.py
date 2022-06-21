import cv2
import numpy as np


all_points = []


def selectPoints(event, x, y, flags, param):
	global all_points
	point = []
	if event == cv2.EVENT_LBUTTONDOWN:
		point.append(x)
		point.append(y)
		all_points.append(point)
		cv2.circle(frame, (x,y), 10, (0,255,0), 10)
		#print(all_points)


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


cap = cv2.VideoCapture('media/video.mp4')
ret, frame = cap.read()
cv2.namedWindow(winname='calibration')
cv2.setMouseCallback('calibration', selectPoints)


while True:
	cv2.imshow('calibration', frame)

	if cv2.waitKey(1) & 0xFF == 27:
		break


pixels_to_cm_conversion_factor = 1 / getAvgDist(all_points)
print("{} pixels per cm".format(1 / pixels_to_cm_conversion_factor))
print("{} cm per pixel".format(pixels_to_cm_conversion_factor))

cv2.destroyAllWindows()

