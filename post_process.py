"""
This program creates pickled files for timestamps and creates a constant mask in the output directory.
"""

from preprocess import *

OUTPUT_DIR = "good_data"
RES_DIR = "res"


def separate_data(timestamps):
	"""Saves pickled lists of timestamps to test.stamps, valid.stamps, and
	train.stamps."""
	test, valid, train = separate_stamps(timestamps)
	with open(OUTPUT_DIR + '/test.stamps', 'wb') as f:
		pickle.dump(test, f)
	with open(OUTPUT_DIR + '/valid.stamps', 'wb') as f:
		pickle.dump(valid, f)
	with open(OUTPUT_DIR + '/train.stamps', 'wb') as f:
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


def extract_times_from_files_in_directory(dir=RES_DIR):
	"""Extracts all timestamps from all the files in the directory given."""
	times = set()
	for file in os.listdir(dir):
		times.update(extract_times_from_file(dir + '/' + file))
	return {t.strip('\n') for t in times}


if __name__ == "__main__":
	times = extract_times_from_files_in_directory()
	separate_data(times)
	create_constant_mask(BLACK, OUTPUT_DIR + '/always_black_mask.png')
