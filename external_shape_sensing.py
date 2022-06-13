import csv
import cv2
import numpy as np
import time


k = 0
vinePositionData = []


def writeData(data):
	with open('data.tsv', 'wt') as out_file:
	    tsv_writer = csv.writer(out_file, delimiter='\t')
	    tsv_writer.writerows(data)



def onMouse(event, x, y, flag, param):
	global ix, iy, k
	if event == cv2.EVENT_LBUTTONDOWN:
		ix, iy = x, y
		k = 1
		return



def trackPoint():

	cap = cv2.VideoCapture('media/video5.mp4')
	cv2.namedWindow('window')
	cv2.setMouseCallback('window', onMouse)

	global k	
	pointData = []
	frame_num = 0

	while True:
		time.sleep(0.1)
		ret, frame = cap.read()
		
		frame_num += 1

		cv2.imshow('window', frame)
	
		if cv2.waitKey(1) & 0xFF == 27 or k==1:
			old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			cv2.destroyAllWindows()
			break
	
	old_points = np.array([ix,iy], dtype = 'float32')
	old_points = old_points.reshape(-1,1,2)
	
	while True:
		ret, frame_new = cap.read()
		frame_num += 1
	
		if not ret:
			break
	
		new_gray = cv2.cvtColor(frame_new, cv2.COLOR_BGR2GRAY)
	
		new_points, status, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, old_points, None, maxLevel=1, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 0.08))
	
		new_x = int(new_points.ravel()[0])
		new_y = int(new_points.ravel()[1])
	
		cv2.circle(frame_new, (new_x,new_y), 10, (0,255,0), 5)
		cv2.imshow('tracking', frame_new)
		
		print('frame: {}'.format(frame_num))
		print('x:{}	y:{}'.format(new_x, new_y))	
		#print('k:{}'.format(k))
		pointData.append([new_x,new_y])
	
		old_gray = new_gray.copy()
		old_points = new_points.copy()
	
		if cv2.waitKey(1) & 0xFF == 27:
			cv2.destroyAllWindows()
			break

	print()
	print()

	add_choice = input("Add this track to output file? (y/n) ")
	if (add_choice.lower() != 'y'):
		print("Track not added.")
	else:
		vinePositionData.append(pointData)
		writeData(vinePositionData)
		print("Track added.")
	print()

	k = 0
	
	cap.release()
	


def main():

	print()
	print("A window will pop up. Wait for a few seconds and then click the point you wish to track.")
	time.sleep(1)
	
	cont = True
	while cont:
		trackPoint()
		cont_choice = input("Track more points? (y/n) ")
		print()
		if (cont_choice.lower() != 'y'):
			cont = False



if __name__ == '__main__':
	main()
