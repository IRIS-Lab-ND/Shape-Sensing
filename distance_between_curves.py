# Calculates the distance between two 3-dimensional curves where each curve
# has the same number of tracked reference points (i.e. marker or gage-points)

import numpy as np
import matplotlib.pyplot as plt


"""Comparison data should be fed in in this format, where x_1, y_1, and z_1
contain relevant collected data from camera-view, and x_2, y_2, and z_2
contain relevant collected data from the LUNA machine. Each file should contain
data where the number of rows corresponds to the number of frames of data collected
and the number of columns corresponds to the number of tracked markers or gage points."""
f_x1 = "luna_data/x_1.txt"
f_y1 = "luna_data/y_1.txt"
f_z1 = "luna_data/z_1.txt"
f_x2 = "luna_data/x_2.txt"
f_y2 = "luna_data/y_2.txt"
f_z2 = "luna_data/z_2.txt"
files = [f_x1, f_y1, f_z1, f_x2, f_y2, f_z2]


# Eventually used to define x axis of graph
num_markers = 0


# Accesses each file and appends x,y,or z data to current 3D point (used in loop)
def examineFile(filename, file_index_number, frame_number, point_1, point_2):
    global num_markers
    point_index_number = file_index_number // 3
    with open(filename) as f:
        line = f.readlines()[frame_number]
        frame_axis_all_points = line.split(",")
        num_markers = len(frame_axis_all_points)
        ctr = 0
        while ctr < num_markers:
            frame_axis_all_points[ctr] = float(frame_axis_all_points[ctr])
            ctr += 1
        if point_index_number == 0:
            point_1.append(frame_axis_all_points)
        else:
            point_2.append(frame_axis_all_points)


# Builds an array of length two which contains two arrays: point 1 and point 2
# Each of these two arrays contains three arrays (x,y,z) whose lengths correspond to
# the number of frames of recorded data.
def getPointsForFrame(frame_number):
    file_index_number = 0
    point_1 = []
    point_2 = []
    for f in files:
        examineFile(f, file_index_number, frame_number, point_1, point_2)
        file_index_number += 1
    points = [point_1, point_2]
    print("POINTS CONSTRUCTED:")
    print(len(points))  # should be 2
    print(len(points[0]))  # should be 3 (x,y,z)
    print(len(points[0][0]))  # should be 1800 (number of markers)
    print(type(points[0][0][0]))  # should print float
    return points


# Two methods (video vs. LUNA) will likely have different durations.
# Used to find the highest number of frames in common.
def getMaxComparisonFrames(axis_from_curve_one, axis_from_curve_two):
    with open(axis_from_curve_one) as a_1:
        number_of_frames_one = len(a_1.readlines())
    with open(axis_from_curve_two) as a_2:
        number_of_frames_two = len(a_2.readlines())
    return min(number_of_frames_one, number_of_frames_two)


# Calculates Euclidean distance in 3D between two points
def getDistanceBetweenTwoPoints(points, marker_num):
    distance = np.sqrt(
        np.square(points[0][0][marker_num] - points[1][0][marker_num])
        + np.square(points[0][1][marker_num] - points[1][1][marker_num])
        + np.square(points[0][2][marker_num] - points[1][2][marker_num])
    )
    return distance


# Goes "frame by frame" (i.e. row-wise in matrix), finds 3D distance between
# points on curve 1 and corresponding points on curve 2, plots all distances for given frame,
# x-axis is marker number/gage point number, y-axis is distance in mm
def graphFrames():
    global num_markers
    max_comparison_frames = getMaxComparisonFrames(f_x1, f_x2)
    frame_number = 0
    while frame_number < max_comparison_frames:
        distances = []
        points = getPointsForFrame(frame_number)
        for i in range(len(points[0][0])):
            distance = getDistanceBetweenTwoPoints(points, i)
            distances.append(distance)
        graph_x_axis_markers = np.linspace(0, num_markers, num_markers)
        plt.plot(graph_x_axis_markers, distances)
        plt.title("Frame {}".format(frame_number))
        plt.xlabel("Marker")
        plt.ylabel("Distance between curves (mm)")
        plt.xlim(0, 2000)
        plt.ylim(0, 700)
        plt.show(block=False)
        plt.pause(0.00000000001)
        plt.close()
        frame_number += 1
        print()


graphFrames()
