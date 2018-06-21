"""
Run this program to create a csv file for each network. Each csv contains the timestamp, fsc_z, fsc_thn_z,
and fsc_opq_z for all of the times that have been processed by the network.
Run this only after process_launch.py has finished processing all of the masks desired.
"""

import os

from process_launch import get_network_mask, get_simple_mask
from utils import extract_exp_label, extract_timestamp


def find_center(mask):
	""" Returns the center of the locations of the first and last non-black pixels and the difference in
	height between them."""
	t, b, l, r = find_circle_boundary(mask)
	r_vertical = (b - t) / 2
	r_horizontal = (r - l) / 2
	return ((t + b) / 2, (l + r) / 2), (r_vertical + r_horizontal) / 2


def find_circle_boundary(mask):
	""" Finds the first non-black pixel in all cardinal directions."""
	answer = []
	flag = False
	for i in range(mask.shape[0]):  # Top
		if flag:
			break
		for j in range(mask.shape[1]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [i]
				flag = True
				break
	flag = False
	for i in range(mask.shape[0] - 1, -1, -1):  # Bottom
		if flag:
			break
		for j in range(mask.shape[1]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [i]
				flag = True
				break
	flag = False
	for j in range(mask.shape[1]):  # Left
		if flag:
			break
		for i in range(mask.shape[0]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [j]
				flag = True
				break
	flag = False
	for j in range(mask.shape[1] - 1, -1, -1):  # Right
		if flag:
			break
		for i in range(mask.shape[0]):
			if tuple(mask[i, j]) != (0, 0, 0):
				answer += [j]
				flag = True
				break
	return answer


def get_fsc(mask, threshold=0.645):
	""" Computes the fractional sky cover from a given mask. By default, computes these values in the zenith region.
	Specify zenith ratio by changing threshold between 0 and 1. Returns total sky cover, opaque sky cover,
	thin sky cover. """
	sky_pixels = 0
	cloud_pixels = 0
	thin_pixels = 0
	t, b, l, r = find_circle_boundary(mask)
	center, rad = find_center(mask)
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
	return (cloud_pixels + thin_pixels) / total, thin_pixels / total, cloud_pixels / total


def get_fsc_from_file(filename):
	"""Computes the fractional sky cover given a filepath."""
	if "simplemask" in filename:
		mask = get_simple_mask(extract_timestamp(filename))
	elif "networkmask" in filename:
		mask = get_network_mask(extract_timestamp(filename), extract_exp_label(filename))
	else:
		return
	return get_fsc(mask)


if __name__ == "__main__":
	exp_labels = ['e70-00', 'e70-01', 'e70-02', 'e70-03', 'e70-04']

	for exp_label in exp_labels:
		name = "fsc_net-" + exp_label
	os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {}" -P 1'.format(name, exp_label))
