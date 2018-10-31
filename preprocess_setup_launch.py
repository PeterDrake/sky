"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) Get the SkyImage and CloudMask data from ARM and unpack tars into your INPUT_DIR (Potentially difficult)
2) Make sure good_data/ and bad_data/ exist and contain shcu_good_data.csv and shcu_bad_data.csv respectively.
3) Run this program. It may take a long time, do not interrupt or you may have to start over from the beginning.

This will create (within good_data and bad_data):
- A folder simpleimage containing folders by year. In this are folders by month and day (mmdd). In each of these
folders are cropped 480x480 sky images
- A folder simplemask with the same structure as simpleimage, but the (mmdd) folders contain cloudmasks which have
been cropped and had the sunband removed.

See the code at the end for a high-level description of the steps this
program goes through.
"""

from random import shuffle
from utils import *

# TODO: Get this to run for both good and bad data in one run
# TODO: Allow skipping of preprocessing if simple files already present in the good and bad data directories

# Constants for input and output locations
INPUT_DIR = '/home/users/jkleiss/TSI_C1'
GOOD_DIR = 'good_data'
GOOD_CSV = 'good_data/shcu_good_data.csv'
BAD_DIR = 'bad_data'
BAD_CSV = 'bad_data/shcu_bad_data.csv'


def create_dirs(timestamps, output_dir):
	"""Creates directories for simpleimage and simplemask in the output_dir as well as creating subdirectories by year
	and day for the given timestamps. Expects the input_dir and output_dir to be relative to the current working
	directory. Pass in an iterable collection of timestamps in the yyyymmddhhmmss format."""
	seen = {}  # yyyy, set(mmdd, ...)
	os.makedirs(output_dir, exist_ok=True)
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


def remove_white_sun(img, stride=10):
	"""Removes the sun disk from img if it is white. (A yellow sun is easier to remove; that is handled directly in
	simplify_masks.) Stride indicates distance between pixels from which sun searches are started"""
	ever_visited = np.full(img.shape[:2], False, dtype=bool)
	visited = np.full(img.shape[:2], False, dtype=bool)
	for r in range(0, img.shape[0], stride):
		for c in range(0, img.shape[1], stride):
			if (img[r][c] == WHITE).all():
				stack = [(r, c)]
				visited.fill(False)
				if depth_first_search(img, visited, ever_visited, stack):
					img[visited] = BLACK
					return img
	# print('No sun found!')
	return img


def depth_first_search(img, visited, ever_visited, stack):
	"""Returns True if there is a connected region including img[r][c] that is all WHITE and surrounded by BLACK.
	Modifies visited to include all of the white pixels. Modifies ever_visited to include all pixels explored."""
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


def crop_image(img):
	"""Expect img to be a numpy array of size 640 x 480. Returns a version of img cropped down to 480 x 480. Axis = 0
	is the vertical axis (i.e. rows) from which the first and last 80 pixels are deleted."""
	return np.delete(img, np.concatenate((np.arange(80), np.arange(80) + 560)), axis=0)


def simplify_image(timestamp, input_dir, output_dir):
	"""Writes simplified versions of mask to simplemask."""
	img_path = extract_img_path_from_time_old(timestamp, input_dir)
	img = misc.imread(img_path)
	img = crop_image(img)
	Image.fromarray(img).save(img_save_path(timestamp, output_dir) + 'simpleimage' + timestamp + '.jpg')
	return


def simplify_mask(timestamp, input_dir, output_dir):
	"""Writes simplified versions of mask to simplemask."""
	mask_path = extract_mask_path_from_time_old(timestamp, input_dir)
	mask = misc.imread(mask_path)
	mask = crop_image(mask)
	if (mask == YELLOW).all(axis=2).any():
		mask[(mask == YELLOW).all(axis=2)] = BLACK
	else:
		mask = remove_white_sun(mask)
	Image.fromarray(mask).save(mask_save_path(timestamp, output_dir) + 'simplemask' + timestamp + '.png')
	return


if __name__ == '__main__':
	# Preprocess GOOD DATA
	print("Beginning to preprocess good data from ", GOOD_CSV)
	print("Removing white spaces.")
	clean_csv(GOOD_CSV)
	print("Extracting timestamps.")
	times = extract_data_from_csv(GOOD_CSV, "timestamp_utc")
	print("Blacklisting timestamps with unpaired images/decision images.")
	blacklist = find_unpaired_images(times, INPUT_DIR)
	times = times - blacklist  # Reassign times to just the ones that are valid
	if blacklist:
		print("Blacklisted the following ", len(blacklist), " timestamps:")
		print(blacklist)
	print("Found ", len(times), " valid image/decision image pairs.")
	print("Creating simpleimage/ and simplemask/ directories in ", GOOD_DIR)
	create_dirs(times, GOOD_DIR)
	print("Beginning image preprocessing from ", INPUT_DIR)
	counter = 0
	for time in times:
		if counter % 1000 == 0:
			print("Percent complete: {0:.0f}%".format(counter / len(times) * 100))
		simplify_mask(time, INPUT_DIR, GOOD_DIR)
		simplify_image(time, INPUT_DIR, GOOD_DIR)
	print("Percent complete: 100%")

	# Preprocess BAD DATA
	print("Beginning to preprocess bad data from ", BAD_CSV)
	print("Removing white spaces.")
	clean_csv(BAD_CSV)
	print("Extracting timestamps.")
	times = extract_data_from_csv(BAD_CSV, "timestamp_utc")
	print("Blacklisting timestamps with unpaired images/decision images.")
	blacklist = find_unpaired_images(times, INPUT_DIR)
	times = times - blacklist  # Reassign times to just the ones that are valid
	if blacklist:
		print("Blacklisted the following ", len(blacklist), " timestamps:")
		print(blacklist)
	print("Found ", len(times), " valid image/decision image pairs.")
	print("Creating simpleimage/ and simplemask/ directories in ", BAD_DIR)
	create_dirs(times, BAD_DIR)
	print("Beginning image preprocessing from ", INPUT_DIR)
	counter = 0
	for time in times:
		if counter % 1000 == 0:
			print("Percent complete: {0:.0f}%".format(counter / len(times) * 100))
		simplify_mask(time, INPUT_DIR, BAD_DIR)
		simplify_image(time, INPUT_DIR, BAD_DIR)
	print("Percent complete: 100%")

	print("Preprocessing complete.")
