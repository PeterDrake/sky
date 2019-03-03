"""
This script can be launched at any time.

Grabs "timestamp_utc" data from a given csv file and separates it into two chunks for later use. One chunk is for
validation/standard plotting, the other is for testing/final plotting. Saves the two chunks into VALID_FILE and
TEST_FILE in the OUTPUT_DIR directory as pickled python lists.
"""

import pickle
from utils import extract_data_from_csv
from config import DUBIOUS_DATA_DIR, DUBIOUS_DATA_CSV

# Set the file names to store the batches in
DUBIOUS_VALID_FILE = DUBIOUS_DATA_DIR + '/poster_valid.stamps'
DUBIOUS_TEST_FILE = DUBIOUS_DATA_DIR + '/poster_test.stamps'

# Set the ratio of validation to total stamps. Ie: RATIO > 0.5 means more validation than testing.
RATIO = 0.6

if __name__ == "__main__":
	times = extract_data_from_csv(DUBIOUS_DATA_CSV, "timestamp_utc")
	timestamps = list(times)
	valid = timestamps[:int(len(timestamps) * RATIO)]
	test = timestamps[int(len(timestamps) * RATIO):]
	with open(DUBIOUS_VALID_FILE, 'wb') as f:
		pickle.dump(valid, f)
	with open(DUBIOUS_TEST_FILE, 'wb') as f:
		pickle.dump(test, f)
