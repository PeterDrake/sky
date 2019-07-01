from utils import *
from config import *
import pandas as pd
import numpy as np
from preprocess import *
import PIL
from PIL import ImageDraw


data = pd.read_csv('shcu_good_sunflag.csv')


sunglare = data['Sflg'] == 1
hglare = data['Hflg'] == 1

# print(data[sunglare]['timestamp_utc'])
# print(data[hglare]['timestamp_utc'])
# print(data[sunglare & hglare]['timestamp_utc'])
#
# print(data[sunglare & hglare]['timestamp_utc'][101990])
#
# print(extract_mask_path_from_time(str(data[sunglare & hglare]['timestamp_utc'][101990]), TYPICAL_DATA_DIR))
# print(extract_img_path_from_time(str(data[sunglare & hglare]['timestamp_utc'][101990]), TYPICAL_DATA_DIR))
#
# print(extract_mask_path_from_time(str(data[sunglare & hglare]['timestamp_utc'][729]), TYPICAL_DATA_DIR))
# print(extract_img_path_from_time(str(data[sunglare & hglare]['timestamp_utc'][729]), TYPICAL_DATA_DIR))


# # mask = np.asarray(imageio.imread('simplemask20120501225700.png', pilmode="RGB"))
# mask = np.asarray(imageio.imread('simplemask20170923235300.png', pilmode="RGB"))
#
#
# i_ = []
# j_ = []
# for i in range(480):
# 	for j in range(480):
# 		# if np.array_equal(mask[i][j], WHITE) or np.array_equal(mask[i][j], GRAY):
# 		# 	mask[i][j] = YELLOW
# 		a = (i - 239) ** 2
# 		b = (j - 239) ** 2
# 		if np.array_equal(mask[i][j], BLACK) and (150 ** 2) < a + b < (206 ** 2):
# 			if i < 240 and 220 < j < 260:
# 				break
# 			else:
# 				# mask[i][j] = YELLOW
# 				i_.append(i)
# 				j_.append(j)
#
# c = int(np.ceil((max(i_) + min(i_))/2))
# d = int(np.ceil((max(j_) + min(j_))/2))
#
# for i in range(480):
# 	for j in range(480):
# 		# if np.array_equal(mask[i][j], WHITE) or np.array_equal(mask[i][j], GRAY):
# 		# 	mask[i][j] = YELLOW
# 		a = (i - c) ** 2
# 		b = (j - d) ** 2
# 		if (np.array_equal(mask[i][j], WHITE) or np.array_equal(mask[i][j], GRAY)) and a + b < (150 ** 2):
# 			mask[i][j] = YELLOW
#
# # imageio.imwrite('simplemask20120501225700_after.png', mask)
# imageio.imwrite('simplemask20170923235300_after.png', mask)

# mask = np.asarray(imageio.imread('simplemask20120501225700.png', pilmode="RGB"))
# sky_image = np.asarray(imageio.imread('simpleimage20120501225700.jpg', pilmode="RGB"))

mask = np.asarray(imageio.imread('simplemask20170923235300.png', pilmode="RGB"))
sky_image = np.asarray(imageio.imread('simpleimage20170923235300.jpg', pilmode="RGB"))

i_ = []
j_ = []
for i in range(480):
	for j in range(480):
		# if np.array_equal(mask[i][j], WHITE) or np.array_equal(mask[i][j], GRAY):
		# 	mask[i][j] = YELLOW
		a = (i - 239) ** 2
		b = (j - 239) ** 2
		if np.array_equal(mask[i][j], BLACK) and (150 ** 2) < a + b < (206 ** 2):
			if i < 240 and 220 < j < 260:
				break
			else:
				# mask[i][j] = YELLOW
				i_.append(i)
				j_.append(j)

c = int(np.ceil((max(i_) + min(i_))/2))
d = int(np.ceil((max(j_) + min(j_))/2))


def add_sunglare(img):
	for i in range(1, 479):
		for j in range(1, 479):
			a = (i - c) ** 2
			b = (j - d) ** 2
			if (np.array_equal(mask[i][j], WHITE) or np.array_equal(mask[i][j], GRAY)) and a + b < (150 ** 2):
				if (np.array_equal(img[i-1][j], YELLOW) or np.array_equal(img[i][j-1], YELLOW) or np.array_equal(img[i+1][j], YELLOW) or np.array_equal(img[i][j+1], YELLOW)) and (np.array_equal(img[i][j], WHITE) or np.array_equal(img[i][j], GRAY)):
					img[i][j] = YELLOW
	return img


for i in range(480):
	for j in range(480):
		if sky_image[i][j][0] > 250 and sky_image[i][j][1] > 250 and sky_image[i][j][2] > 250:
			if np.array_equal(mask[i][j], BLACK):
				break
			else:
				mask[i][j] = YELLOW

# for i in range(10):
# 	mask = add_sunglare(mask)

imageio.imwrite('simplemask20170923235300_after.png', mask)

# im = Image.open('simplemask20170923235300_after.png')
# ImageDraw.floodfill(im, (5, 5), (255, 255, 0))
# im.save('trial.png', "PNG")

for i in range(480):
	for j in range(480):
		# a = (i - c) ** 2
		# b = (j - d) ** 2
		# if a + b < (150 ** 2):
			if np.array_equal(mask[i][j], YELLOW):
				if np.array_equal(mask[i][j+1], WHITE) or np.array_equal(mask[i][j+1], GRAY):
					im = Image.open('simplemask20170923235300_after.png')
					ImageDraw.floodfill(im, (i, j+1), (255, 255, 0))
					im.save('trial.png', "PNG")



# imageio.imwrite('simpleimage20120501225700_after.png', sky_image)
# imageio.imwrite('simplemask20120501225700_after.png', mask)

imageio.imwrite('simplemask20170923235300_after.png', mask)