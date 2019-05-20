import numpy as np
import os
import pickle
import time
from PIL import Image
from scipy import misc
from utils import extract_data_from_csv, extract_times_from_files_in_directory, separate_data, BLACK, BLUE
from config import TYPICAL_DATA_DIR, DUBIOUS_DATA_DIR, DUBIOUS_DATA_CSV


def create_constant_mask(color, filename):
	"""Creates a mask where any pixels not always of color are BLUE. Saves it in filename."""
	b_mask = np.full((480, 480, 3), color)
	for dirpath, subdirs, files in os.walk(TYPICAL_DATA_DIR + '/simplemask/'):
		for file in files:
			img = misc.imread(os.path.join(dirpath, file))
			b_mask[(img != color).any(axis=2)] = BLUE
	Image.fromarray(b_mask.astype('uint8')).save(filename)


def setup(train, valid, test):
	times = extract_times_from_files_in_directory(TYPICAL_DATA_DIR + "/res")
	separate_data(times, train, valid, test)
	create_constant_mask(BLACK, TYPICAL_DATA_DIR + '/always_black_mask.png')


if __name__ == "__main__":
	start = time.clock()
	# For typical data
	print("Creating training, validation, and test stamps for typical data")
	train_stamp_path = TYPICAL_DATA_DIR + '/train.stamps'
	valid_stamp_path = TYPICAL_DATA_DIR + '/valid.stamps'
	test_stamp_path = TYPICAL_DATA_DIR + '/test.stamps'
	setup(train_stamp_path, valid_stamp_path, test_stamp_path)
	print("Finished. Stamps saved at: ", train_stamp_path, ", ", valid_stamp_path, ", ", test_stamp_path)

	# For dubious data
	print("Creating validation and test stamps for dubious data")
	valid_stamp_path = DUBIOUS_DATA_DIR + '/poster_valid.stamps'  # TODO: Rename these to valid and test .stamps
	test_stamp_path = DUBIOUS_DATA_DIR + '/poster_test.stamps'
	ratio_valid_test = 0.6  # The ratio of validation to testing data for dubious data.
	timestamps = extract_data_from_csv(DUBIOUS_DATA_CSV, "timestamp_utc")
	timestamps = list(timestamps)
	valid_stamps = timestamps[:int(len(timestamps) * ratio_valid_test)]
	test_stamps = timestamps[int(len(timestamps) * ratio_valid_test):]
	with open(valid_stamp_path, 'wb') as f:
		pickle.dump(valid_stamps, f)
	with open(test_stamp_path, 'wb') as f:
		pickle.dump(test_stamps, f)
	print("Finished. Stamps saved at: ", valid_stamp_path, ", ", test_stamp_path)
	print("Time elapsed: " + str(time.clock() - start) + " seconds.")
