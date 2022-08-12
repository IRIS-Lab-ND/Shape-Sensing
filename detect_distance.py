import cv2

from realsense_depth import *

point = (1,1)
def show_distance(event, x, y, args, params):
    global point
    point = (x,y)



dc = DepthCamera()

cv2.namedWindow("color frame")
cv2.setMouseCallback("color frame", show_distance)

while True:
    ret, depth_frame, color_frame = dc.get_frame()

    cv2.circle(color_frame, point, 4, (0,0,255))
    distance = depth_frame[point[1], point[0]]
    print(distance)


    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("color frame", color_frame)
    if cv2.waitKey(1) == 27:
        break
