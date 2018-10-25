"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) Get the SkyImage and CloudMask data from ARM and unpack tars into your INPUT_DIR
2) Specify the OUTPUT_DIR (which need not already exist).
3) Specify BATCH_SIZE to help parallelize this process. This is the number of timestamps each batch needs to process.
To run sequentially instead of in parallel, set this absurdly high.
4) Run this program, wait for it to finish.
5) Run preprocess_launch.py to do the actual simplification of masks & cropping of images
6) Once that is done, run preprocess_stamps_launch.py to separate stamps into training, validation, and testing batches.

This will create (within data):
- A folder simpleimage containing folders by year. In this are folders by month and day (mmdd). In these folders are
cropped 480x480 sky images
- A folder simplemask with the same structure as simpleimage, but the (mmdd) folders contain cloudmasks which have
been cropped and had the sunband removed.

See the code at the end for a high-level description of the steps this
program goes through.

Written by Zoe Harrington & Maxwell Levin
"""

from random import shuffle
from utils import *

# Constants for input and output locations
INPUT_DIR = '/home/users/jkleiss/TSI_C1'
OUTPUT_DIR = 'bad_data'
RES_DIR = OUTPUT_DIR + '/res'
TIMESTAMP_DATA_CSV = 'bad_data/shcu_good_data.csv'  # shcu_bad_data has about 5,000 times, shcu_good_data has about 100,000 times

# Used to create batches of timestamps. This is the number of images to preprocess in a single job.
# We suggest using 1000 for bad_data, and 5000 to 10000 for good_data if using a cluster
BATCH_SIZE = 1000


def create_dirs(timestamps, output_dir, res_dir):
	"""Creates directories for simpleimage and simplemask in the output_dir as well as creating subdirectories by year
	and day for the given timestamps. Expects the input_dir and output_dir to be relative to the current working
	directory. Pass in an iterable collection of timestamps in the yyyymmddhhmmss format."""
	seen = {}  # yyyy, set(mmdd, ...)
	os.makedirs(output_dir, exist_ok=True)
	os.makedirs(res_dir, exist_ok=True)
	for t in timestamps:
		year = time_to_year(t)
		mmdd = time_to_month_and_day(t)
		if year not in seen.keys():
			seen[year] = set()
		seen[year].add(mmdd)
	for year in seen.keys():
		os.makedirs(output_dir + "/simpleimage/" + year, exist_ok=True)
		os.makedirs(output_dir + "/simplemask/" + year, exist_ok=True)
		for mmdd in seen[year]:
			os.makedirs(output_dir + "/simpleimage/" + year + "/" + mmdd, exist_ok=True)
			os.makedirs(output_dir + "/simplemask/" + year + "/" + mmdd, exist_ok=True)
	return


def make_batches_by_size(timestamps, batch_size=BATCH_SIZE):
	"""Returns a set of batches of timestamps. The number of batches is determined by the length of the timestamps
	collection and the number of elements in a batch can be provided by the user. batch_size is set to 10000 by
	default as a best guess at the trade-off between parallelization and practicality."""
	timestamps = list(timestamps)
	num_batches = math.ceil(len(timestamps) / batch_size)
	shuffle(timestamps)
	time_batches = []
	for i in range(int(num_batches) - 1):
		time_batches += [timestamps[i * batch_size:(i + 1) * batch_size]]
	time_batches.append(timestamps[(num_batches - 1) * batch_size:])
	return time_batches


if __name__ == '__main__':
	print("Cleaning the csv file.")
	clean_csv(TIMESTAMP_DATA_CSV)

	print("Reading times from good csv file.")
	good_times = extract_data_from_csv(TIMESTAMP_DATA_CSV, "timestamp_utc")

	print("Finished reading times. Eliminating unpaired times.")
	blacklist = find_unpaired_images(good_times, INPUT_DIR)
	times = good_times - blacklist

	print("{} paired images and masks found.".format(len(times)))
	print("Creating directories for results.")
	create_dirs(times, OUTPUT_DIR, RES_DIR)

	print("Directories created. Preparing batches.")
	batches = make_batches_by_size(times)

	print("Batches prepared. Writing batches to file.")
	for i in range(len(batches)):
		name = RES_DIR + "/batch" + str(i) + ".txt"
		if not os.path.isfile(name):  # TODO Do we need this?
			f = open(name, 'w')
			print("Writing batch {} data to {}".format(i, name))
			for time in batches[i]:
				f.write(time + '\n')
			f.close()
		else:
			print("{} already exists, continuing to launch.".format(name))

	print("Timestamp files complete.")
