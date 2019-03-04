"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) Get the SkyImage and CloudMask data from ARM and unpack tars into your RAW_DATA_DIR
2) Specify the OUTPUT_DIR (which need not already exist). We set this to 'typical_data' and 'dubious_data'
3) Specify PREPROCESS_BATCH_SIZE to help parallelize this process. This is the number of timestamps each batch needs to process.
To run sequentially instead of in parallel, set this absurdly high.
4) Run this program, wait for it to finish.
5) Run preprocess_launch.py to do the actual simplification of masks & cropping of images
6) Once that is done, run preprocess_stamps_launch.py to separate stamps into training, validation, and testing batches.

This will create (within data):
- A folder simpleimage containing folders by year. In this are folders by month and day (mmdd). In these folders are
cropped 480x480 sky images
- A folder simplemask with the same structure as simpleimage, but the (mmdd) folders contain cloudmasks which have
been cropped and had the sunband removed.

See the code at the end for a high-level description of the steps this program goes through.
"""

from config import *
from random import shuffle
from utils import *


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


def make_batches_by_size(timestamps, batch_size=PREPROCESS_BATCH_SIZE):
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


def setup(output_dir, timestamp_data_csv):
	res_dir = output_dir + '/res'
	print("Cleaning the csv file.")
	clean_csv(timestamp_data_csv)
	print("Reading times from typical csv file.")
	timestamps = extract_data_from_csv(timestamp_data_csv, "timestamp_utc")
	# This can be used to process a small amount images instead of everything specified by the csv files.
	if SMALL_PROCESS_SIZE:
		print("Reducing the number of timestamps to around ", SMALL_PROCESS_SIZE)
		few_times = set()
		count = 0
		for t in timestamps:
			few_times.add(t)
			count += 1
			if count == SMALL_PROCESS_SIZE:
				break
		timestamps = few_times
	print("Finished reading times. Eliminating unpaired times.")
	blacklist = find_unpaired_images(timestamps, RAW_DATA_DIR)
	times = timestamps - blacklist
	print("{} paired images and masks found.".format(len(times)))
	print("Creating directories for results.")
	create_dirs(times, output_dir, res_dir)
	print("Directories created. Preparing batches.")
	batches = make_batches_by_size(times)
	print("Batches prepared. Writing batches to file.")
	for i in range(len(batches)):
		name = res_dir + "/batch" + str(i) + ".txt"
		f = open(name, 'w')
		print("Writing batch {} data to {}".format(i, name))
		for time in batches[i]:
			f.write(time + '\n')
		f.close()
	print("Timestamp files complete.")


if __name__ == '__main__':
	setup(TYPICAL_DATA_DIR, TYPICAL_DATA_CSV)
	setup(DUBIOUS_DATA_DIR, DUBIOUS_DATA_CSV)  # TODO: Is the batch file here ever used?
