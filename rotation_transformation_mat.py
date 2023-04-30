import numpy as np
import pandas as pd
import csv 
import time

# returns an array of length 3 containing the vector between two points
def get_vector(point_1, point_2):
	v = [point_2[0]-point_1[0], point_2[1]-point_1[1], point_2[2]-point_1[2]]
	return v


# returns the magnitude (scalar) of a vector
def get_vector_magnitude(vector):
	m = np.linalg.norm(vector)
	return m



# returns array of unit vectors *in correct order* based on patent
# i.e., parallel = z, perpendicular = x, upwards = y 
def get_unit_vectors(calibration_map, origin_LED, parallel_LED, perpendicular_LED):
	luna_parallel_vector = get_vector(calibration_map.get(origin_LED), calibration_map.get(parallel_LED))
	luna_parallel_magnitude = get_vector_magnitude(luna_parallel_vector)
	luna_parallel_uv = luna_parallel_vector / luna_parallel_magnitude

	luna_perpendicular_vector = get_vector(calibration_map.get(origin_LED), calibration_map.get(perpendicular_LED))
	luna_perpendicular_magnitude = get_vector_magnitude(luna_perpendicular_vector)
	luna_perpendicular_uv = luna_perpendicular_vector / luna_perpendicular_magnitude

	luna_upwards_uv = np.cross(luna_parallel_uv, luna_perpendicular_uv)

	unit_vectors_arr = [luna_perpendicular_uv, luna_upwards_uv, luna_parallel_uv]
	
	return unit_vectors_arr



def main():

	# gets user input
	phasespace_filename = "luna_data/LunaComparisonTest2.csv"
	origin_LED = int(input("Origin LED Number (0-6): "))
	parallel_LED = int(input("LED Number running parallel to LUNA strain (0-6): "))
	perpendicular_LED = int(input("LED Number perpendicular to LUNA strain (0-6): "))
	total_LEDS_active = int(input("Total number of LEDs active during PhaseSpace data collection: "))

	# declares empty arrays and counter variables
	calibration_arr= []
	calibration_map = {}
	rowcount = 0

	# context manager csv file reader
	with open(phasespace_filename) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			row_arr = []

			# checks that we are in the first frame of data (used for calibration) and that we are in one of the specified LEDs' rows 
			if (rowcount>=12 and rowcount <=19 and (int(row[2]) == origin_LED or int(row[2]) == parallel_LED or int(row[2]) == perpendicular_LED)):
				# appends columns containing x,y,z
				row_arr.append(row[3])
				row_arr.append(row[4])
				row_arr.append(row[5])
				calibration_arr.append(row_arr) # adds one of three LEDs to a 2D array 

				# maps each coordinate set (x,y,z) to its corresponding LED
				if(origin_LED == int(row[2])):
					calibration_map[origin_LED] = row_arr
				elif(parallel_LED == int(row[2])):
					calibration_map[parallel_LED] = row_arr
				elif(perpendicular_LED == int(row[2])):
					calibration_map[perpendicular_LED] = row_arr
			
			# exits the loop once relevant data has been gotten so that the program doesn't have to iterate through 2345094285 rows needlessly
			if (rowcount >= 13 + total_LEDS_active * 2):
				break
			rowcount += 1



	# converts the three points of interest to float since they are read in as strings
	for i in range(0,len(calibration_arr)):
		for j in range(0,len(calibration_arr)):
			calibration_arr[i][j] = float(calibration_arr[i][j])

	

	# checks that the coordinate sets are stored in the correct order by fetching them by LED number
	#print(calibration_map.get(origin_LED))
	#print(calibration_map.get(parallel_LED))
	#print(calibration_map.get(perpendicular_LED))


	# outputs an array (3x3) of unit vectors
	unit_vectors_array = get_unit_vectors(calibration_map, origin_LED, parallel_LED, perpendicular_LED)

	# prints origin coordinates	
	print()
	print("Origin of LUNA in PhaseSpace coordinates: {}".format(calibration_map.get(origin_LED)))

	# prints unit vector array
	print("Unit vectors array: {}",format(unit_vectors_array))


	print()

	# creates r_pl where unit vectors are stores as *row vectors*
	r_pl = [ [unit_vectors_array[0][0],	unit_vectors_array[0][1], unit_vectors_array[0][2]],
		 [unit_vectors_array[1][0],	unit_vectors_array[1][1], unit_vectors_array[1][2]],
		 [unit_vectors_array[2][0],	unit_vectors_array[2][1], unit_vectors_array[2][2]],
		]

	# creates r_pl where unit vectors are stores as *column vectors*
	r_pl = [ [unit_vectors_array[0][0],	unit_vectors_array[1][0], unit_vectors_array[2][0]],
		 [unit_vectors_array[0][1],	unit_vectors_array[1][1], unit_vectors_array[2][1]],
		 [unit_vectors_array[0][2],	unit_vectors_array[1][2], unit_vectors_array[2][2]],
		]
	r_pl_np = np.asarray(r_pl)	
	pd.DataFrame(r_pl_np).to_csv("r_pl.csv")


	p_lp = np.array([[calibration_map.get(origin_LED)[0]],
			[calibration_map.get(origin_LED)[1]],
			[calibration_map.get(origin_LED)[2]]])

	print(p_lp)
	t_pl_np = np.append(r_pl_np, p_lp, axis=1)
	t_pl_np = np.append(t_pl_np, [0, 0, 0, 1])
	pd.DataFrame(t_pl_np).to_csv("t_pl.csv")

	print()
	print("R_PL")
	print(r_pl_np)
	print()
	print("T_PL")
	print(t_pl_np)



if __name__ == "__main__":
	main()
