import math
import os
import pickle

import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
from scipy import misc

from preprocess_setup_launch import INPUT_DIR, extract_img_path_from_time_old, extract_mask_path_from_time_old
from show_output import out_to_image, read_last_iteration_number, read_parameters
from train import build_net, load_inputs


def time_to_year(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the year as a string."""
	return str(time)[0:4]


def time_to_month(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the month as a string."""
	return str(time)[4:6]


def time_to_day(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the day as a string."""
	return str(time)[6:8]


def time_to_month_and_day(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the 'mmdd'."""
	return str(time)[4:8]


def time_to_year_month_day(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the 'yyyymmdd'."""
	return str(time)[0:8]


def time_to_hour_minute_second(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the 'hhmmss'."""
	return str(time)[8:14]


def extract_timestamp(filename):
	"""Returns the timestamp within filename. Assumes filename ends in something like 20160415235930.jpg or
	20160415235930.png."""
	return filename[-18:-4]


def extract_exp_label(filename):
	"""Returns the experiment label within filename of networkmasks. Assumes filename ends in something like
	e70-00.20160415235930.png"""
	return filename[-25:-19]


def extract_all_times(dir, subdirs=None):
	"""Returns timestamps from all directories that are within the input directory. You can specify a list of
	subdirectories if you only want to grab files within specific subdirectories.
	Ex: dir/masks/mask20160411000000.jpg would be extracted, and
		dir/masks/folder/mask20160411000000.jpg would also be extracted."""
	times = set()
	if not subdirs:
		for dirpath, subdirs, files in os.walk(dir):
			for file in files:
				times.add(extract_timestamp(file))
	else:
		for subdir in subdirs:
			for dirpath, subdirs, files in os.walk(dir + subdir):
				for file in files:
					times.add(extract_timestamp(file))
	return times


def extract_times_from_filenames(filenames):
	"""Returns an iterable of timestamps extracted from an iterable collection of files."""
	return {extract_timestamp(filename) for filename in filenames}


def extract_times_from_file(filename):
	"""Returns a set of timestamps in a given file. Assumes timestamps are separated by newlines."""
	times = set()
	with open(filename, 'r') as file:
		for time in file:
			times.add(str(time))
	return times


def extract_data_from_csv(filename, column_header):
	"""Returns a list of data from a csv file. Assumes the csv has headers."""
	data = pd.read_csv(filename).get(column_header)
	return {str(d) for d in data}


def extract_tsi_fsc_for_bad_dates(timestamps):
	nan_fsc = set()
	csv = read_csv_file("shcu_good_data.csv")
	df = csv.set_index("timestamp_utc", drop=False)
	# drop=False to not delete timestamp_utc column if other index set later
	for time in timestamps:
		fsc_value = df.loc[time, "fsc_z"]
		if fsc_value == 0:
			nan_fsc.add(time)
	return nan_fsc


def extract_tsi_fsc_for_date(timestamp):
	csv = read_csv_file("shcu_good_data.csv")
	df = csv.set_index("timestamp_utc", drop=False)
	# drop=False to not delete timestamp_utc column if other index set later
	return (math.floor(df.loc[timestamp, "fsc_z"] * 10 ** 6)) / 10 ** 6


def extract_ceilometer_fsc_for_date(timestamp):
	csv = read_csv_file("shcu_good_data.csv")
	df = csv.set_index("timestamp_utc", drop=False)
	# drop=False to not delete timestamp_utc column if other index set later
	return (math.floor(df.loc[timestamp, "cf_tot"] * 10 ** 6)) / 10 ** 6


def read_csv_file(filename):
	"""Reads a csv file using the pandas csv reader and returns a pandas data frame."""
	return pd.read_csv(filename)


def listdir_d(dir=None):
	"""Returns an iterable of directories in the current or a given directory."""
	return (name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name)))


def listdir_f(dir=None):
	"""Returns an iterable of files in the current of a given directory."""
	return (name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name)))


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


def show_skymask(mask, save_instead=False, save_path=None):
	""" Shows the mask for a given timestamp, alternatively can show a given mask."""
	mask_image = Image.fromarray(mask.astype('uint8'))
	if not save_instead:
		mask_image.show()
	else:
		mask_image.save(save_path)


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
		path = 'results/' + exp_label + '/masks/' + time_to_year(timestamp) + '/' + time_to_month_and_day(
				timestamp) + '/networkmask_' + exp_label + '.' + timestamp + '.png'
	return os.path.isfile(path)


def find_unpaired_images(timestamps, input_dir=INPUT_DIR):
	"""Blacklists files for timestamps that do not have both images and masks."""
	blacklist = set()
	for time in timestamps:
		mask = extract_mask_path_from_time_old(time, input_dir)
		image = extract_img_path_from_time_old(time, input_dir)
		if not os.path.isfile(mask) or not os.path.isfile(image):
			blacklist.add(time)
		elif os.path.getsize(mask) == 0 or os.path.getsize(image) == 0:
			blacklist.add(time)
	return blacklist


def extract_img_path_from_time(time, input_dir=INPUT_DIR):
	"""Extracts the path of an image from the timestamp and input directory."""
	return input_dir + '/' + 'simpleimage/' + time_to_year(time) + '/' + time_to_month_and_day(
			time) + '/simpleimage' + time + '.jpg'


def extract_mask_path_from_time(time, input_dir=INPUT_DIR):
	"""Extracts the path of an image from the timestamp and input directory."""
	return input_dir + '/' + 'simplemask/' + time_to_year(time) + '/' + time_to_month_and_day(
			time) + '/simplemask' + time + '.png'


def img_save_path(time, dir):
	"""Creates path for image."""
	return dir + '/' + 'simpleimage/' + time_to_year(time) + '/' + time_to_month_and_day(time) + '/'


def mask_save_path(time, dir):
	"""Creates path for mask."""
	return dir + '/' + 'simplemask/' + time_to_year(time) + '/' + time_to_month_and_day(time) + '/'


def separate_data(timestamps):
	"""Saves pickled lists of timestamps to test.stamps, valid.stamps, and
	train.stamps."""
	test, valid, train = separate_stamps(timestamps)
	with open('test.stamps', 'wb') as f:
		pickle.dump(test, f)
	with open('valid.stamps', 'wb') as f:
		pickle.dump(valid, f)
	with open('train.stamps', 'wb') as f:
		pickle.dump(train, f)
	return test, valid, train


def separate_stamps(timestamps):
	"""Shuffles stamps and returns three lists: 20% of the stamps for
	testing, 16% for validation, and the rest for training."""
	timestamps = list(timestamps)
	test = timestamps[0:int(len(timestamps) * 0.2)]
	valid = timestamps[int(len(timestamps) * 0.2):int(len(timestamps) * 0.4)]
	train = timestamps[int(len(timestamps) * 0.4):]
	return test, valid, train
