#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finds the zenith area of TSI skymasks
"""

import random

from analyze import *


# DONE: Make sure fsc is easily computed from simplified masks
# DONE: Grab fsc info from shcu_good_data csv file (and possibly other files in the future)
# DONE?: Read in some new masks from our network in good_data


# TODO: Loosely compare between the different methods. The csv info should agree with the simplified masks,
# TODO: hopefully the network outputs as well.
# TODO: Be able to display simple masks and network output for images with the most disagreement


# TODO: Look into reading this as a uint8 image
def get_simple_mask(timestamp, input_dir='good_data'):
	""" Returns the mask of a given timestamp in the input data directory. Assumes the timestamp is organized in the
	input dir so that input_dir/simplemask/2017/0215/simplemask20170215000000.png is the filepath for the timestamp
	20170215000000."""
	return np.array(misc.imread(extract_mask_path_from_time(timestamp, input_dir)))


def get_network_mask(timestamp, exp_label):
	"""Returns the mask of a given timestamp from the network's output."""
	network_dir = "results/" + exp_label + "/"
	args = read_parameters(network_dir)
	step_version = read_last_iteration_number(network_dir)
	layer_info = args['Layer info'].split()
	_, _, saver, _, x, y, _, _ = build_net(layer_info)
	with tf.Session() as sess:
		saver.restore(sess, network_dir + 'weights-' + str(step_version))
		img = load_inputs([timestamp])
		mask = out_to_image(y.eval(feed_dict={x: img}))[0]
	return mask


def get_network_masks(timestamps, exp_label):
	"""Returns a list of masks that have been processed by the network and saves each one in the network directory. """
	network_dir = "results/" + exp_label + "/"
	args = read_parameters(network_dir)
	step_version = read_last_iteration_number(network_dir)
	layer_info = args['Layer info'].split()
	_, _, saver, _, x, y, _, _ = build_net(layer_info)
	masks = []
	with tf.Session() as sess:
		saver.restore(sess, network_dir + 'weights-' + str(step_version))
		for t in timestamps:
			inputs = load_inputs([t])
			result = out_to_image(y.eval(feed_dict={x: inputs}))[0]
			masks.append(result)
			save_network_mask(t, exp_label, result)
	return masks


def show_skymask(mask, save_instead=False, save_path=None):
	""" Shows the mask for a given timestamp, alternatively can show a given mask."""
	mask_image = Image.fromarray(mask.astype('uint8'))
	if not save_instead:
		mask_image.show()
	else:
		mask_image.save(save_path)


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
	return (cloud_pixels + thin_pixels) / total, cloud_pixels / total


def save_network_mask(timestamp, exp_label, mask=None):
	"""Saves the skymasks created by the neural network in results/experiment_label/masks/year/monthday/
	eg. results/e70-00/masks/2016/0904/ and creates filename eg. networkmask_e70-00.20160904233000.png"""
	if not mask:
		mask = get_network_mask(timestamp, exp_label)
	path = 'results/' + exp_label + '/masks/' + time_to_year(timestamp) + '/' + time_to_month_and_day(
			timestamp) + '/'
	os.makedirs(path, exist_ok=True)
	file = 'networkmask_' + exp_label + '.' + timestamp + '.png'
	show_skymask(mask, save_instead=True, save_path=path + file)


def get_fsc_from_file(filename):
	"""Computes the fractional sky cover given a filepath."""
	if "simplemask" in filename:
		mask = get_simple_mask(extract_timestamp(filename))
	elif "networkmask" in filename:
		mask = get_network_mask(extract_timestamp(filename), extract_exp_label(filename))
	else:
		return
	return get_fsc(mask)


if __name__ == '__main__':
	times = extract_data_from_csv('shcu_good_data.csv', 'timestamp_utc')
	times = random.sample(times, 5)

	exp_labels = ('e70-00', 'e70-01', 'e70-02', 'e70-03', 'e70-04')
	for label in exp_labels:
		masks = get_network_masks(times, label)
