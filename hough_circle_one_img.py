import cv2
import numpy as np
import os

path = "typical_data/hough_circle_sample_files/"
dirs = os.listdir(path)

for file in dirs:
	print(file)
	img = cv2.imread(path + file, 0)
	# img = cv2.medianBlur(img, 5)
	cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	# minRadius=210, maxRadius=245
	circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 120, param1=70, param2=50, minRadius=200, maxRadius=250)

	circles = np.uint16(np.around(circles))
	print(len(circles))
	for i in circles[0]:
		# draw the outer circle
		cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
		# draw the center of the circle
		cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
		# center of circle
		print('center of circle: ' + str((i[0], i[1])))
		# radius
		print('radius: ' + str(i[2]))


	cv2.imshow('detected circles', cimg)
	cv2.waitKey(0)
cv2.destroyAllWindows()

