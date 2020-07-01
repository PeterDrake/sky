import numpy as np
import os
import pickle
import time
from PIL import Image
from utils import extract_data_from_csv, extract_times_from_files_in_directory, separate_data, BLACK, BLUE
from config import TYPICAL_DATA_DIR, DUBIOUS_DATA_DIR, DUBIOUS_DATA_CSV
import imageio


def create_constant_mask(color, filename, filepath):
	"""
	Creates a mask where any pixels not always of color are BLUE. This mask is used later
	so that the system won't have to learn to classify the pixels that are the same color in all TSI decision images.
	:param color: Pixels not this color in all TSI decision image will be BLUE in the saved image.
	:param filename: File (including full pathname) to write output image.
	:param filepath: Directory containing TSI decision images (possibly in subdirectories).
	"""
	b_mask = np.full((480, 480, 3), color)
	for dirpath, subdirs, files in os.walk(filepath):
		for file in files:
			print("Constant mask includes " + file)
			img = np.asarray(imageio.imread(os.path.join(dirpath, file)))
			print(img.shape)
			b_mask[(img != color).any(axis=2)] = BLUE
	Image.fromarray(b_mask.astype('uint8')).save(filename)


def create_stamps(train, valid, test):
	"""Creates .stamps files which contains timestamps of the dataset. These files are
	divided by percentages determined in the separate_data function. Also creates constant mask."""
	times = extract_times_from_files_in_directory(TYPICAL_DATA_DIR + "/res")
	separate_data(times, train, valid, test)
	create_constant_mask(BLACK, TYPICAL_DATA_DIR + '/always_black_mask.png', TYPICAL_DATA_DIR + '/simplemask/')


def create_typical_data_stamps():
	global train_stamp_path, valid_stamp_path, test_stamp_path
	train_stamp_path = TYPICAL_DATA_DIR + '/train.stamps'
	valid_stamp_path = TYPICAL_DATA_DIR + '/valid.stamps'
	test_stamp_path = TYPICAL_DATA_DIR + '/test.stamps'
	create_stamps(train_stamp_path, valid_stamp_path, test_stamp_path)


def create_dubious_data_stamps():
	global valid_stamp_path, test_stamp_path
	valid_stamp_path = DUBIOUS_DATA_DIR + '/valid.stamps'
	test_stamp_path = DUBIOUS_DATA_DIR + '/test.stamps'
	ratio_valid_test = 0.6  # The ratio of validation to testing data for dubious data.
	timestamps = extract_data_from_csv(DUBIOUS_DATA_CSV, "timestamp_utc")
	timestamps = list(timestamps)
	valid_stamps = timestamps[:int(len(timestamps) * ratio_valid_test)]
	test_stamps = timestamps[int(len(timestamps) * ratio_valid_test):]
	with open(valid_stamp_path, 'wb') as f:
		pickle.dump(valid_stamps, f)
	with open(test_stamp_path, 'wb') as f:
		pickle.dump(test_stamps, f)


if __name__ == "__main__":
	start = time.clock()
	print("Creating training, validation, and test stamps for typical data")
	create_typical_data_stamps()
	print("Finished. Stamps saved at: ", train_stamp_path, ", ", valid_stamp_path, ", ", test_stamp_path)
	print("Creating validation and test stamps for dubious data")
	create_dubious_data_stamps()
	print("Finished. Stamps saved at: ", valid_stamp_path, ", ", test_stamp_path)
	print("Time elapsed: " + str(time.clock() - start) + " seconds.")
