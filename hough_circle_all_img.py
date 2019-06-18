import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from config import RAW_DATA_DIR, TYPICAL_DATA_DIR
from utils import extract_img_path_from_time_raw


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
		print('radius: ' + radius)
		print('center of circle: ' + circle_center)
	file.close()
	print("Finished preprocessing sky and decision images in ", filename)


def hough_circle(timestamp, input_dir):
	img_path = extract_img_path_from_time_raw(timestamp, input_dir)
	print('img_path: ' + img_path)
	img = cv.imread(img_path, 0)

	circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 100, param1=60, param2=90, minRadius=200, maxRadius=0)

	circles = np.uint16(np.around(circles))

	for i in circles[0]:

		# center of circle
		circle_center = (i[0], i[1])
		print('center of circle: ' + str((i[0], i[1])))

		# radius
		radius = i[2]
		print('radius: ' + str(i[2]) + '\n')

	return radius, circle_center

if __name__ == "__main__":
	# batches = os.listdir(TYPICAL_DATA_DIR + '/res')
	# for batch in enumerate(batches):
	# 	hough_preprocess(TYPICAL_DATA_DIR + '/res/' + str(batch))
	hough_preprocess(TYPICAL_DATA_DIR + '/res/batch0.txt')

# SGE_Batch -r "hough_circle" -c "python3 -u hough_circle_all_img.py" -P 1
