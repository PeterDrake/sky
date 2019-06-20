import cv2 as cv
import numpy as np
import math
from config import RAW_DATA_DIR, TYPICAL_DATA_DIR
from utils import extract_img_path_from_time_raw
import pandas as pd


def hough_preprocess(filename):
	"""Simplifies sky and decision images given a filename containing timestamps and an output_dir to save the
	simplified images."""
	file = open(filename)
	print("Opened {}".format(filename))
	for time in file:
		time = time.replace('\n', '')
		time = time.replace(' ', '')
		print('time: ' + time)
		radius, circle_center = hough_circle(time, RAW_DATA_DIR)
		print('radius: ' + str(radius))
		print('center of circle: ' + str(circle_center))
		global data
		data.append({'time': time, 'y': circle_center[1], 'x': circle_center[0], 'radius': radius})
	file.close()
	print("Finished preprocessing sky and decision images in ", filename)


def hough_circle(timestamp, input_dir):
	img_path = extract_img_path_from_time_raw(timestamp, input_dir)
	img = cv.imread(img_path, 0)
	img = cv.medianBlur(img, 11)

	circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 70, param1=30, param2=7,
							  minRadius=224, maxRadius=245)

	if circles is None:
		return 0, (0, 0)

	circles = np.uint16(np.around(circles))

	closest_points_to_center = (999, 999)
	old_distance = 60
	radius = 999

	for i in circles[0, :]:

		distance = math.sqrt(((240 - i[0]) ** 2) + ((320 - i[1]) ** 2))

		if distance < old_distance:
			old_distance = distance
			closest_points_to_center = (i[0], i[1])
			radius = i[2]

	return radius, closest_points_to_center


if __name__ == "__main__":
	# batches = os.listdir(TYPICAL_DATA_DIR + '/res')
	# for batch in enumerate(batches):
	# 	hough_preprocess(TYPICAL_DATA_DIR + '/res/' + str(batch))

	data = []
	hough_preprocess(TYPICAL_DATA_DIR + '/res/batch0.txt')
	hough_centers = pd.DataFrame(data)
	hough_centers.to_csv('hough_centers_2.csv')

# SGE_Batch -r "hough_circle" -c "python3 -u hough_circle_all_img.py" -P 1
