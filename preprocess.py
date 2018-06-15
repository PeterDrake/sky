"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) Get the SkyImage and CloudMask data from ARM and unpack tars into your INPUT_DIR
2) Specify the OUTPUT_DIR (which need not already exist).
3) Specify BATCH_SIZE to help parallelize this process. This is the number of timestamps each batch needs to process.
To run sequentially, set this absurdly high.
4) Run this program, wait for it to finish.
5) Run process.py to do the actual simplification of masks & cropping of images

# TODO All of the steps in preprocess, process, and postprocess should count as preprocessing.

This will create (within data):

- A folder simpleimage containing folders by year. In this are folders by month and day (mmdd). In these folders are
cropped 480x480 sky images
- A folder simplemask with the same structure as simpleimage, but the (mmdd) folders contain cloudmasks which have
been cropped and had the sunband removed.

See the code at the end for a high-level description of the steps this
program goes through.

Written by Zoe Harrington & Maxwell Levin
"""

import glob
import math
import pickle
from random import shuffle

import numpy as np
from PIL import Image
from scipy import misc

from util import *

# These constants are colors that appear in cloud masks
WHITE = np.array([255, 255, 255])
BLUE = np.array([0, 0, 255])
GRAY = np.array([192, 192, 192])
BLACK = np.array([0, 0, 0])
GREEN = np.array([0, 255, 0])
YELLOW = np.array([255, 255, 0])
COLORS = (WHITE, BLUE, GRAY, BLACK, GREEN)

# Constants for input and output locations
INPUT_DIR = '/home/users/jkleiss/TSI_C1'
OUTPUT_DIR = 'good_data'
RES_DIR = 'res'

# Size of each batch, should be able to specify via command-line
BATCH_SIZE = 10000


def create_dirs(times, output_dir=OUTPUT_DIR, res_dir=RES_DIR):
	"""Creates directories for simpleimage and simplemask in the output_dir as well as creating subdirectories by year
	and day for the given timestamps. Expects the input_dir and output_dir to be relative to the current working
	directory. Pass in an iterable collection of timestamps in the yyyymmddhhmmss format."""
	seen = {}  # yyyy, set(mmdd, ...)
	os.makedirs("output_dir", exist_ok=True)
	os.makedirs(res_dir, exist_ok=True)
	for t in times:
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


def crop_image(img):
	"""Expect img to be a numpy array of size 640 x 480. Returns a version of img cropped down to 480 x 480.
	Axis = 0 is the vertical axis (i.e. rows) from which the first and last 80 pixels are deleted."""
	return np.delete(img, np.concatenate((np.arange(80), np.arange(80) + 560)), axis=0)


def create_constant_mask(color, filename):
	"""Creates a mask where any pixels not always of color are BLUE. Saves it in filename."""
	b_mask = np.full((480, 480, 3), color)
	for _, _, files in os.walk(OUTPUT_DIR + '/simplemask/'):
		for file in files:
			img = misc.imread(OUTPUT_DIR + '/simplemask/' + file)
			b_mask[(img != color).any(axis=2)] = BLUE
	Image.fromarray(b_mask.astype('uint8')).save(OUTPUT_DIR + '/' + filename)


def depth_first_search(r, c, img, visited, ever_visited, stack):
	"""Returns True if there is a connected region including img[r][c] that is all
	WHITE and surrounded by BLACK. Modifies visited to include all of the white pixels.
	Modified ever_visited to include all pixels explored."""
	while stack:
		r, c = stack.pop()
		if (img[r][c] == BLACK).all():
			continue
		if visited[r][c]:
			continue
		visited[r][c] = True
		if ever_visited[r][c]:
			return False
		ever_visited[r][c] = True
		if (img[r][c] == GREEN).all() or (img[r][c] == BLUE).all() or (img[r][c] == GRAY).all():
			return False
		stack.extend(((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
	return True


def find_unpaired_images(timestamps, input_dir=INPUT_DIR):
	"""Blacklists files for timestamps that do not have both images and masks."""
	blacklist = set()
	for time in timestamps:
		mask = extract_mask_path_from_time(time, input_dir)
		image = extract_img_path_from_time(time, input_dir)
		if not os.path.isfile(mask) or not os.path.isfile(image):
			blacklist.add(time)
		elif os.path.getsize(mask) == 0 or os.path.getsize(image) == 0:
			blacklist.add(time)
	return blacklist


def extract_img_path_from_time(time, input_dir=INPUT_DIR):
	"""Extracts the path of an image from the timestamp and input directory."""
	for dir in glob.glob(input_dir + '/SkyImage/' + 'sgptsiskyimageC1.a1.' + time_to_year_month_day(time) + '*'):
		image = dir + '/' + 'sgptsiskyimageC1.a1.' + time_to_year_month_day(time) + '.' + time_to_hour_minute_second(
				time) + '.jpg.' + time + '.jpg'
		if os.path.isfile(image):
			return image
	return str()


def extract_mask_path_from_time(time, input_dir=INPUT_DIR):
	"""Extracts the path of a mask from the timestamp and input directory."""
	mask = input_dir + '/CloudMask/' + 'sgptsicldmaskC1.a1.' + time_to_year_month_day(
			time) + '/' + 'sgptsicldmaskC1.a1.' + time_to_year_month_day(time) + '.' + time_to_hour_minute_second(
			time) + '.png.' + time + '.png'
	return mask


def remove_white_sun(img, stride=10):
	"""Removes the sun disk from img if it is white. (A yellow sun is easier
	to remove; that is handled directly in simplify_masks.) Stride indicates distance
	between pixels from which sun searches are started"""
	# start = time.clock()
	ever_visited = np.full(img.shape[:2], False, dtype=bool)
	visited = np.full(img.shape[:2], False, dtype=bool)
	for r in range(0, img.shape[0], stride):
		for c in range(0, img.shape[1], stride):
			if ((img[r][c] == WHITE).all()):
				stack = []
				stack.append((r, c))
				visited.fill(False)
				if depth_first_search(r, c, img, visited, ever_visited, stack):
					img[visited] = BLACK
					# print('Removed the sun in ' + str(time.clock() - start) + ' seconds')
					return img
	print('No sun found!')
	return img


def img_save_path(time, dir):
	"""Creates path for image."""
	return dir + '/' + 'simpleimage/' + time_to_year(time) + '/' + time_to_month_and_day(time) + '/'


def mask_save_path(time, dir):
	"""Creates path for mask."""
	return dir + '/' + 'simplemask/' + time_to_year(time) + '/' + time_to_month_and_day(time) + '/'


def simplify_image(timestamp, input_dir=INPUT_DIR, output_dir=OUTPUT_DIR):
	"""Writes simplified versions of mask to simplemask."""
	img_path = extract_img_path_from_time(timestamp, input_dir)
	img = misc.imread(img_path)
	img = crop_image(img)
	Image.fromarray(img).save(img_save_path(timestamp, output_dir) + 'simpleimage' + timestamp + '.jpg')
	return


def simplify_mask(timestamp, input_dir=INPUT_DIR, output_dir=OUTPUT_DIR):
	"""Writes simplified versions of mask to simplemask. """
	mask_path = extract_mask_path_from_time(timestamp, input_dir)
	mask = misc.imread(mask_path)
	mask = crop_image(mask)
	if (mask == YELLOW).all(axis=2).any():
		mask[(mask == YELLOW).all(axis=2)] = BLACK
	else:
		mask = remove_white_sun(mask)
	Image.fromarray(mask).save(mask_save_path(timestamp, output_dir) + 'simplemask' + timestamp + '.png')
	return


def make_batches_by_size(timestamps, batch_size=BATCH_SIZE):
	"""Returns a set of batches of timestamps. The number of batches is determined by the length of the timestamps
	collection and the number of elements in a batch can be provided by the user. batch_size is set to 10000 by
	default as a best guess at the trade-off between parallelization and practicality."""
	timestamps = list(timestamps)
	num_batches = math.ceil(len(timestamps) / batch_size)
	shuffle(timestamps)
	batches = []
	for i in range(int(num_batches) - 1):
		batches += [timestamps[i * batch_size:(i + 1) * batch_size]]
	batches.append(timestamps[(num_batches - 1) * batch_size:])
	return batches


def launch_blt_simplify_task(filename):
	"""Launches run_batch.py to preprocess the data in parallel on blt."""
	os.system('SGE_Batch -r "{}" -c "python3 -u run_batch.py {}" -P 1'.format(filename[4:-4], filename))


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


def preprocess(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR, res_dir=RES_DIR):
	"""Launches the preprocess task, which creates the appropriate directories and creates text files to store
	timestamps."""
	print("Reading times from good csv file.")
	good_times = extract_data_from_csv("shcu_good_data.csv", "timestamp_utc")
	print("Finished reading times. Eliminating unpaired times.")
	blacklist = find_unpaired_images(good_times, INPUT_DIR)
	times = good_times - blacklist
	print("{} paired images and masks found.".format(len(times)))
	print("Creating directories for results.")
	create_dirs(times, OUTPUT_DIR)
	print("Directories created. Preparing batches.")
	batches = make_batches_by_size(times)
	print("Batches created. Launching simplification on batches.")
	for i in range(len(batches)):
		name = res_dir + "/batch" + str(i) + ".txt"
		if not os.path.isfile(name):  # TODO Do we need this?
			f = open(name, 'w')
			print("Writing batch {} data to {}".format(i, name))
			for time in batches[i]:
				f.write(time + '\n')
			f.close()
		else:
			print("{} already exists, continuing to launch.".format(name))
	print("Timestamp files complete.")


if __name__ == '__main__':
	preprocess()
