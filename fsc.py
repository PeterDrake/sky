#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finds the zenith area of TSI skymasks
"""

import numpy as np
from PIL import Image
from scipy import misc


def get_mask(timestamp):
	return np.array(misc.imread('data/simplemask/simplemask' + str(timestamp) + '.png'))


def show_skymask(timestamp, mask=None):
	if not mask.any():
		mask = get_mask(timestamp)
	mask_image = Image.fromarray(mask.astype('uint8'))
	mask_image.show()


# numpy array (480, 480, 3) go through find first non black pixel
def find_first_non_black_pixel(timestamp, mask=None):
	if not mask.any():
		mask = get_mask(timestamp)
	for i in range(mask.shape[0]):
		for j in range(mask.shape[1]):
			if tuple(mask[i, j]) != (0, 0, 0):
				print(i, j)
				mask[i, j] = [255, 0, 0]
				return i, j


def find_second_non_black_pixel(timestamp, mask=None):
	if not mask.any():
		mask = get_mask(timestamp)
	print(mask[0])
	for i in range(mask.shape[0]):
		for j in range(mask.shape[1] - 1, -1, -1):
			if tuple(mask[i, j]) != (0, 0, 0):
				print(mask.shape[0] - 4 - i, j)
				mask[mask.shape[0] - 4 - i, j] = [255, 0, 255]
				return mask.shape[0] - 4 - i, j


def find_center(timestamp, mask=None):
	p1 = find_first_non_black_pixel(timestamp, mask)
	p2 = find_second_non_black_pixel(timestamp, mask)
	return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2), (p2[0] - p1[0]) / 2


def get_pixels_in_center(timestamp, mask=None):
	center, r = find_center(timestamp, mask)
	new_r = 0.6 * r
	new_mask = mask.copy()
	for i in range(mask.shape[0]):
		for j in range(mask.shape[1]):
			if (i - center[0]) ** 2 + (j - center[1]) ** 2 > new_r ** 2:
				new_mask[i, j] = [0, 0, 0]
	return np.array(new_mask)


def get_fsc(mask):
	sky_pixels = 0
	cloud_pixels = 0
	for i in range(mask.shape[0]):
		for j in range(mask.shape[1]):
			color = tuple(mask[i, j])
			if color == (0, 0, 0):
				continue
			elif color == (0, 0, 255):
				sky_pixels += 1
			elif color == (0, 255, 0):
				continue
			else:
				cloud_pixels += 1
	return cloud_pixels / (cloud_pixels + sky_pixels)


# for index, x in np.ndenumerate(mask):
#
# #black = 3
#
# # top
# for i in np.nditer():
#     if
#
#         img = misc.imread('simplemask/' + file)
#         b_mask[(img != color).any(axis=2)] = BLUE


# preproccess.py simplify_all_masks to get all skymasks

if __name__ == '__main__':
	timestamp = 20160414162830
	mask = get_mask(timestamp)
	# find_first_non_black_pixel(timestamp, mask)
	# find_second_non_black_pixel(timestamp, mask)
	show_skymask(timestamp, mask)
	# print(find_center(timestamp,mask))
	print(get_fsc(get_pixels_in_center(timestamp, mask)))
