import csv
import cv2
import numpy as np
import time

from calibration import pixels_per_cm
from calibration import origin_x
from calibration import origin_y

k = 0
vine_position_data_x = []
vine_position_data_y = []
total_frame_count = 0



def writeData(data, data_filename):
	with open(data_filename,'a') as out_file:
	    tsv_writer = csv.writer(out_file, delimiter='\t')
	    tsv_writer.writerows(data)



def onMouse(event, x, y, flag, param):
	global ix, iy, k
	if event == cv2.EVENT_LBUTTONDOWN:
		ix, iy = x, y
		k = 1
		return



def trackPoint(video_filename):

	cap = cv2.VideoCapture(video_filename)
	cv2.namedWindow('window')
	cv2.setMouseCallback('window', onMouse)

	global k
	global total_frame_count	
	point_data_x = [None] * (total_frame_count + 1)
	point_data_y = [None] * (total_frame_count + 1)
	point_data_x[0] = "Point"
	point_data_y[0] = "Point"
	idx = 0

	ret, frame = cap.read()
	while True:
		
		cv2.imshow('window', frame)
		time.sleep(0.1)
	
		if cv2.waitKey(1) & 0xFF == 27 or k==1:
			old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			cv2.destroyAllWindows()
			break
	
	old_points = np.array([ix,iy], dtype = 'float32')
	old_points = old_points.reshape(-1,1,2)
	
	while True:
		ret, frame_new = cap.read()
		idx += 1 
		if not ret:
			break
	
		new_gray = cv2.cvtColor(frame_new, cv2.COLOR_BGR2GRAY)
	
		new_points, status, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, old_points, None, maxLevel=1, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 0.08))
	
		new_x = int(new_points.ravel()[0])
		new_y = int(new_points.ravel()[1])
	
		cv2.circle(frame_new, (new_x,new_y), 10, (0,255,0), 5)
		cv2.circle(frame_new, (origin_x,origin_y), 10, (0,255,0), 5)
		cv2.line(frame_new, pt1=(new_x, new_y), pt2=(origin_x, origin_y), color=(102,255,255), thickness = 3)
		cv2.imshow('tracking', frame_new)
		
		print('frame: {}'.format(idx))
		print('absolute x pixels:{}	absolute y pixels:{}'.format(new_x, new_y))	

		dist_to_origin_x_pixels = origin_x - new_x
		dist_to_origin_y_pixels = origin_y - new_y
		print('adjusted x pixels:{}	adjusted y pixels:{}'.format(dist_to_origin_x_pixels, dist_to_origin_y_pixels))

		dist_to_origin_x_scaled = dist_to_origin_x_pixels / pixels_per_cm
		dist_to_origin_y_scaled = dist_to_origin_y_pixels / pixels_per_cm
		print('scaled x distance: {}cm		scaled y distance:{}cm'.format(dist_to_origin_x_scaled, dist_to_origin_y_scaled))

		point_data_x[idx] = dist_to_origin_y_scaled
		point_data_y[idx] = dist_to_origin_y_scaled
	
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
		vine_position_data_x.append(point_data_x)
		vine_position_data_y.append(point_data_y)
		print("Track added.")
	print()

	k = 0
	
	cap.release()



def populateFrameColumns(video_filename):
	global total_frame_count
	cap_temp = cv2.VideoCapture(video_filename)
	total_frame_count = int(cap_temp.get(cv2.CAP_PROP_FRAME_COUNT))
	row = [i for i in range(0,total_frame_count+1)]
	row[0] = None
	with open('pos_x.tsv', 'wt') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		tsv_writer.writerow(row)
	with open('pos_y.tsv', 'wt') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		tsv_writer.writerow(row)



def main():
	
	video_filename = 'media/video.mp4'
	populateFrameColumns(video_filename)


	print()
	print("A window will pop up. Wait for a few seconds and then click the point you wish to track.")
	time.sleep(1)
	
	cont = True
	while cont:
		trackPoint(video_filename)
		cont_choice = input("Track more points? (y/n) ")
		print()
		if (cont_choice.lower() != 'y'):
			cont = False

	writeData(vine_position_data_x, 'pos_x.tsv')
	writeData(vine_position_data_y, 'pos_y.tsv')


if __name__ == '__main__':
	main()
