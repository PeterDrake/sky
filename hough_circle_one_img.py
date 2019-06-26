import cv2
import numpy as np
import os
import math

path = "typical_data/hough_circle_sample_files/"
dirs = os.listdir(path)

for file in dirs:
	# print(file)
	img = cv2.imread(path + file, 0)
	img = cv2.medianBlur(img, 11)
	cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	# minRadius=210, maxRadius=245
	circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 70, param1=30, param2=7,
							   minRadius=224, maxRadius=243)

	circles = np.uint16(np.around(circles))
	closest_to_center = (240, 320)
	old_distance = 60
	for i in circles[0, :]:

		distance = math.sqrt(((240 - i[0]) ** 2) + ((320 - i[1]) ** 2))

		if distance < old_distance:
			old_distance = distance
			closest_to_center = (i[0], i[1])
			radius = i[2]

		# draw the outer circle
		# cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 1)
		# # test circle
		# cv2.circle(cimg, (i[0], i[1]), 245, (255, 255, 0), 1)
		# cv2.circle(cimg, (i[0], i[1]), 220, (255, 255, 0), 1)
		# # draw the center of the circle
		# cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
		# # center of circle

	cv2.circle(cimg, (closest_to_center[0], closest_to_center[1]), 2, (255, 0, 255), 3)
	cv2.circle(cimg, (closest_to_center[0], closest_to_center[1]), radius, (255, 0, 255), 1)
	cv2.circle(cimg, (240, 320), 60, (255, 0, 255), 1)

	print('{} {} {} {}'.format(file, closest_to_center[0], closest_to_center[1], radius))
	# radius
	# print('radius: ' + str(i[2]))


	cv2.imshow('detected circles', cimg)
	cv2.waitKey(0)
cv2.destroyAllWindows()

