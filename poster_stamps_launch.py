import pickle


def separate_data(timestamps, output_dir=None, test_ratio=0.4, valid_ratio=0.6):
	"""Saves pickled lists of timestamps to test.stamps, valid.stamps, and
	train.stamps."""
	if output_dir:
		output_dir = output_dir + '/'
	test, valid = separate_stamps(timestamps, test_ratio, valid_ratio)
	with open(output_dir + 'test.stamps', 'wb') as f:
		pickle.dump(test, f)
	with open(output_dir + 'valid.stamps', 'wb') as f:
		pickle.dump(valid, f)
	return test, valid


def separate_stamps(timestamps, test_ratio, valid_ratio):
	"""Shuffles stamps and returns three lists: 20% of the stamps for
	testing, 16% for validation, and the rest for training."""
	if test_ratio + valid_ratio == 1:
		timestamps = list(timestamps)
		test = timestamps[0:int(len(timestamps) * test_ratio)]
		valid = timestamps[int(len(timestamps) * (test_ratio + valid_ratio)):]
		return test, valid
