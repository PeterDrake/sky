from preprocess import *

OUTPUT_DIR = "good_data"
RES_DIR = "res"


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


def extract_times_from_files_in_directory(dir=RES_DIR):
	"""Extracts all timestamps from all the files in the directory given."""
	times = set()
	for file in os.listdir(dir):
		times.update(extract_times_from_file(dir + '/' + file))
	return times


if __name__ == "__main__":
	times = extract_times_from_files_in_directory()
	separate_data(times)
