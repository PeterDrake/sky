"""
This script can be launched at any time.

Grabs "timestamp_utc" data from a given csv file and separates it into two chunks for later use. One chunk is for
validation/standard plotting, the other is for testing/final plotting. Saves the two chunks into VALID_FILE and
TEST_FILE as pickled python lists.
"""

import pickle
from utils import extract_data_from_csv

# Set the csv file containing the timestamps to set
INPUT_DATA_CSV = 'shcu_bad_data.csv'

# Set the filenames to store the batches in
VALID_FILE = 'poster_valid.stamps'
TEST_FILE = 'poster_test.stamps'

# Set the ratio of validation to total stamps. Ie: RATIO > 0.5 means more validation than testing.
RATIO = 0.6

# TODO: Shuffle the times before writing it to a list.
if __name__ == "__main__":
	times = extract_data_from_csv(INPUT_DATA_CSV, "timestamp_utc")
	timestamps = list(times)
	valid = timestamps[:int(len(timestamps) * RATIO)]
	test = timestamps[int(len(timestamps) * RATIO):]
	with open(VALID_FILE, 'wb') as f:
		pickle.dump(valid, f)
	with open(TEST_FILE, 'wb') as f:
		pickle.dump(test, f)
