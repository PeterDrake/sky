#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finds the zenith area of TSI skymasks
"""

import numpy as np
from PIL import Image
from scipy import misc
from preprocess import *


# TODO: Make sure fsc is easily computed from simplified masks
# TODO: Grab fsc info from shcu_good_data csv file (and possibly other files in the future)
# TODO: Read in some new masks from our network in good_data

# TODO: Loosely compare between the different methods. The csv info should agree with the simplified masks,
# hopefully the network outputs as well.
# TODO: Be able to display simple masks and network output for images with the most disagreement


# TODO: Look into reading this as a uint8 image
def get_mask(timestamp, input_dir='good_data'):
	""" Returns the mask of a given timestamp in the simplemask data directory. Does not handle exceptions."""
	try:
		return np.array(misc.imread(extract_mask_path_from_time(timestamp, input_dir)))  # Good_data type of format
	except OSError:
		print("Error reading in file. Are you sure {} has an existing mask in the input directory?")

def show_skymask(timestamp, mask=None):
	""" Shows the mask for a given timestamp, alternatively can show a given mask."""
	if mask is None:
		mask = get_mask(timestamp)
	mask_image = Image.fromarray(mask.astype('uint8'))
	mask_image.show()


def find_circle_boundary(timestamp, mask=None):
	""" Finds the first non-black pixel in all cardinal directions."""
	if mask is None:
		mask = get_mask(timestamp)
	answer = []
	flag = False
	# Top
	for i in range(mask.shape[0]):
		if flag:
			break
		for j in range(mask.shape[1]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [i]
				flag = True
				break
	# Bottom
	flag = False
	for i in range(mask.shape[0] - 1, -1, -1):
		if flag:
			break
		for j in range(mask.shape[1]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [i]
				flag = True
				break
	# Left
	flag = False
	for j in range(mask.shape[1]):
		if flag:
			break
		for i in range(mask.shape[0]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [j]
				flag = True
				break
	# Right
	flag = False
	for j in range(mask.shape[1] - 1, -1, -1):
		if flag:
			break
		for i in range(mask.shape[0]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [j]
				flag = True
				break
	return answer


def find_center(timestamp, mask=None):
	""" Returns the center of the locations of the first and last non-black pixels and the difference in
	height between them."""
	t, b, l, r = find_circle_boundary(timestamp, mask)
	r_vertical = (b - t) / 2
	r_horizontal = (r - l) / 2
	return ((t + b) / 2, (l + r) / 2), (r_vertical + r_horizontal) / 2


# def get_pixels_in_center(timestamp, mask=None, threshold=0.645):
# 	""" Returns a new image mask containing pixels that are within a threshold of the center of the mask."""
# 	center, r = find_center(timestamp, mask)
# 	new_r = threshold * r
# 	new_mask = mask.copy()
# 	for i in range(mask.shape[0]):
# 		for j in range(mask.shape[1]):
# 			if (i - center[0]) ** 2 + (j - center[1]) ** 2 > new_r ** 2:
# 				new_mask[i, j] = [0, 0, 0]
# 	return new_mask


def get_fsc(timestamp, mask=None, threshold=0.645):
	""" Computes the fractional sky cover from a given mask. Returns total sky cover, opaque sky cover."""
	if mask is None:
		mask = get_mask(timestamp)
	sky_pixels = 0
	cloud_pixels = 0
	thin_pixels = 0
	t, b, l, r = find_circle_boundary(timestamp, mask)
	center, rad = find_center(timestamp, mask)
	new_r = threshold * rad
	for i in range(t, b + 1):
		for j in range(l, r + 1):
			if (i - center[0]) ** 2 + (j - center[1]) ** 2 > new_r ** 2:
				# mask[i, j] = [0, 0, 0] # Uncomment this to show the portion used to calculate fsc
				continue
			color = tuple(mask[i, j])
			if color == (0, 0, 0) or color == (0, 255, 0):
				continue
			elif color == (0, 0, 255):
				sky_pixels += 1
			elif color == (255, 255, 255):
				cloud_pixels += 1
			else:
				thin_pixels += 1
	total = sky_pixels + cloud_pixels + thin_pixels
	return (cloud_pixels + thin_pixels) / total, cloud_pixels / total


def get_whole_fsc(timestamp, mask=None):
	""" Computes the fractional sky cover from a given mask. Returns total sky cover, opaque sky cover."""
	if mask is None:
		mask = get_mask(timestamp)
	sky_pixels = 0
	cloud_pixels = 0
	thin_pixels = 0
	t, b, l, r = find_circle_boundary(timestamp, mask)
	center, rad = find_center(timestamp, mask)
	for i in range(t, b + 1):
		for j in range(l, r + 1):
			if (i - center[0]) ** 2 + (j - center[1]) ** 2 > rad ** 2:
				# mask[i, j] = [0, 0, 0] # Uncomment this to show the portion used to calculate fsc
				continue
			color = tuple(mask[i, j])
			if color == (0, 0, 0) or color == (0, 255, 0):
				continue
			elif color == (0, 0, 255):
				sky_pixels += 1
			elif color == (255, 255, 255):
				cloud_pixels += 1
			else:
				thin_pixels += 1
	total = sky_pixels + cloud_pixels + thin_pixels
	return (cloud_pixels + thin_pixels) / total, cloud_pixels / total


# def get_fsc2(mask):
# 	""" Computes the fractional sky cover from a given mask. Returns total sky cover, opaque sky cover."""
# 	sky_pixels = 0
# 	cloud_pixels = 0
# 	thin_pixels = 0
# 	for i in range(mask.shape[0]):
# 		for j in range(mask.shape[1]):
# 			color = tuple(mask[i, j])
# 			if color == (0, 0, 0):
# 				continue
# 			elif color == (0, 0, 255):
# 				sky_pixels += 1
# 			elif color == (0, 255, 0):
# 				continue
# 			elif color == (255, 255, 255):q
# 				cloud_pixels += 1
# 			else:
# 				thin_pixels += 1
# 	total = sky_pixels + cloud_pixels + thin_pixels
# 	return (cloud_pixels + thin_pixels) / total, cloud_pixels / total


if __name__ == '__main__':
	pass
# stamp = 20160414162830
# # stamp = 20160530192700
# mask = get_mask(stamp)
# show_skymask(stamp)
#
# # new_mask = get_pixels_in_center(stamp, mask)
# # fsc = get_fsc2(new_mask)
# # print(fsc)
# # show_skymask(stamp, new_mask)
#
# fsc1, fsc2 = get_fsc(stamp, mask)
# print(fsc1, fsc2)
#
# fsc1, fsc2 = get_whole_fsc(stamp, mask)
# print(fsc1, fsc2)
