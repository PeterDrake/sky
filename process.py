"""
This is called by process_launch.
Processes sky images into cloud masks. Requires command line arguments for the experiment label, starting index,
and ending index. Experiment label is to specify the directory in which the network is stored WITHIN the results
directory.
"""

import sys
import tensorflow as tf

from utils import *
from train import build_net, load_inputs
from config import RESULTS_DIR, EXPERIMENT_LABEL


# TODO: Implement this in utils
def read_last_iteration_number(network_dir):
	"""Returns something like weights-XXXX, which is the filename (without extension) of the saved network."""
	filename = glob.glob(network_dir + "weights-*")
	i = filename[0].index("weights-") + len("weights-")
	iteration_number = int(filename[0][i:].split('.')[0])
	return iteration_number


def process_network_masks(timestamps, exp_label, input_dir):
	"""Processes images corresponding to a list of timestamps. Saves each mask in the network directory. Does NOT
	check to make sure that the image exists. This must be done by the user before calling this method."""
	network_dir = RESULTS_DIR + '/' + exp_label + '/'
	args = read_parameters(network_dir)
	step_version = read_last_iteration_number(network_dir)
	layer_info = args['Layer info'].split()
	_, _, saver, _, x, y, _, _ = build_net(layer_info)
	# masks = []
	with tf.Session() as sess:
		saver.restore(sess, network_dir + 'weights-' + str(step_version))
		for t in timestamps:
			inputs = load_inputs([t], input_dir)
			result = out_to_image(y.eval(feed_dict={x: inputs}))[0]
			# masks.append(result)
			save_network_mask(t, exp_label, result)
	# return masks


def get_network_mask(timestamp, exp_label, input_dir):
	"""Returns the mask of a given timestamp from the network's output."""
	network_dir = RESULTS_DIR + '/' + exp_label + '/'
	args = read_parameters(network_dir)
	step_version = read_last_iteration_number(network_dir)
	layer_info = args['Layer info'].split()
	_, _, saver, _, x, y, _, _ = build_net(layer_info)
	with tf.Session() as sess:
		saver.restore(sess, network_dir + 'weights-' + str(step_version))
		img = load_inputs([timestamp], input_dir)
		mask = out_to_image(y.eval(feed_dict={x: img}))[0]
	return mask


def save_network_mask(timestamp, exp_label, mask=None):
	"""Saves the skymasks created by the neural network in results/experiment_label/masks/year/monthday/
	eg. results/e70-00/masks/2016/0904/ and creates filename eg. networkmask_e70-00.20160904233000.png"""
	if mask is None:
		mask = get_network_mask(timestamp, exp_label)
	path = RESULTS_DIR + '/' + exp_label + '/masks/' + time_to_year(timestamp) + '/' + time_to_month_and_day(
		timestamp) + '/'
	os.makedirs(path, exist_ok=True)
	file = 'networkmask_' + exp_label + '.' + timestamp + '.png'
	show_skymask(mask, save_instead=True, save_path=path + file)


def network_output_exists(timestamp, exp_label, path=None):
	"""Returns true if the mask has already been created, false otherwise."""
	if path is None:
		path = extract_network_mask_path_from_time(timestamp, exp_label)
	return os.path.isfile(path)


def process(start, finish, input_directory, input_csv):
	temp = sorted(list(extract_data_from_csv(input_csv, 'timestamp_utc')))[start:finish]
	times = []
	for t in temp:
		if not network_output_exists(t, EXPERIMENT_LABEL):
			if os.path.isfile(extract_img_path_from_time(t, input_directory)):
				if os.path.getsize(extract_img_path_from_time(t, input_directory)) != 0:
					times.append(t)
	process_network_masks(times, EXPERIMENT_LABEL, input_directory)


if __name__ == '__main__':
	s = int(sys.argv[1])  # Starting index of the timestamp in the typical_data/shcu_typical_data.csv file
	f = int(sys.argv[2])  # Final timestamp to consider
	input_dir = sys.argv[3]
	input_data_csv = sys.argv[4]
	process(s, f, input_dir, input_data_csv)
