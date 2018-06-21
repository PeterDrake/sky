"""
Call this program after completing all preprocess launch tasks. This method goes through all cropped sky images and
produces the network output mask for each. Breaks up tasks into many smaller batches to improve speed. Specify the
number of batches per network to increase the number of batches created & increase speed. Make sure that the number
of batches times the number of batches per network is small enough so that BLT can fit all of the jobs.
"""

import os

import numpy as np
import tensorflow as tf
from scipy import misc

from train import build_net, load_inputs
from utils import extract_mask_path_from_time, out_to_image, read_last_iteration_number, read_parameters, \
	show_skymask, \
	time_to_month_and_day, time_to_year


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


def process_network_masks(timestamps, exp_label):
	"""Processes images corresponding to a list of timestamps. Saves each mask in the network directory. Does NOT
	check to make sure that the image exists. This must be done by the user before calling this method."""
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


def get_network_mask_path(timestamp, exp_label):
	"""Returns the save path of a network mask. The mask does not necessarily need to exist."""
	return 'results/' + exp_label + '/masks/' + time_to_year(timestamp) + '/' + time_to_month_and_day(
			timestamp) + '/networkmask_' + exp_label + '.' + timestamp + '.png'


def save_network_mask(timestamp, exp_label, mask=None):
	"""Saves the skymasks created by the neural network in results/experiment_label/masks/year/monthday/
	eg. results/e70-00/masks/2016/0904/ and creates filename eg. networkmask_e70-00.20160904233000.png"""
	if mask is None:
		mask = get_network_mask(timestamp, exp_label)
	path = 'results/' + exp_label + '/masks/' + time_to_year(timestamp) + '/' + time_to_month_and_day(
			timestamp) + '/'
	os.makedirs(path, exist_ok=True)
	file = 'networkmask_' + exp_label + '.' + timestamp + '.png'
	show_skymask(mask, save_instead=True, save_path=path + file)


def network_output_exists(timestamp, exp_label, path=None):
	"""Returns true if the mask has already been created, false otherwise."""
	if path is None:
		path = get_network_mask_path(timestamp, exp_label)
	return os.path.isfile(path)


if __name__ == "__main__":
	exp_labels = ['e70-00', 'e70-01', 'e70-02', 'e70-03', 'e70-04']

	num_batches = len(exp_labels)
	num_batches_per_network = 5

	total_length = -1  # This file has a header
	for line in open('shcu_good_data.csv'):
		total_length += 1

	batch_length = int(total_length / num_batches_per_network)

	for exp_label in exp_labels:
		for i in range(num_batches_per_network):
			name = "net-" + exp_label + "-" + str(i)
			start = batch_length * i
			finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
			os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {} {} {}" -P 1'.format(name, exp_label, start, finish))
