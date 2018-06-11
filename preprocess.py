import glob

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


def create_dirs(times, output_dir):
	"""Creates directories for simpleimage and simplemask in the output_dir as well as creating subdirectories by year
	and day for the given timestamps. Expects the input_dir and output_dir to be relative to the current working
	directory. Pass in an iterable collection of timestamps in the yyyymmddhhmmss format."""
	seen = {}  # yyyy, set(mmdd, ...)
	for t in times:
		year = time_to_year(t)
		mmdd = time_to_month_and_day(t)
		if year not in seen.keys():
			seen[year] = set()
		seen[year].add(mmdd)
	for year in seen.keys():
		os.makedirs(output_dir + "/simpleimage/" + year)
		os.makedirs(output_dir + "/simplemask/" + year)
		for mmdd in seen[year]:
			os.makedirs(output_dir + "/simpleimage/" + year + "/" + mmdd)
			os.makedirs(output_dir + "/simplemask/" + year + "/" + mmdd)
	return


def crop_image(img):
	"""Expect img to be a numpy array of size 640 x 480. Returns a version of img cropped down to 480 x 480.
	Axis = 0 is the vertical axis (i.e. rows) from which the first and last 80 pixels are deleted."""
	return np.delete(img, np.concatenate((np.arange(80), np.arange(80) + 560)), axis=0)


def count_colors(img):
	"""Returns an array of the number of WHITE, BLUE, GRAY, BLACK, and
	GREEN pixels in img."""
	counts = [(img == color).all(axis=2).sum() for color in COLORS]
	return np.array(counts)


def depth_first_search(r, c, img, visited, ever_visited, stack):
	"""Returns True if there is a connected region including img[r][c] that is all
	WHITE and surrounded by BLACK. Modifies visited to include all of the white pixels.
	Modified ever_visited to include all pixels explored."""
	while stack:
		r, c = stack.pop()
		if ((img[r][c] == BLACK).all()):
			continue
		if (visited[r][c]):
			continue
		visited[r][c] = True
		if (ever_visited[r][c]):
			return False
		ever_visited[r][c] = True
		if (img[r][c] == GREEN).all() or (img[r][c] == BLUE).all() or (img[r][c] == GRAY).all():
			return False
		stack.extend(((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
	return True


def find_unpaired_images(input_dir, timestamps):
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


def extract_img_path_from_time(time, input_dir):
	"""Extracts the path of an image from the timestamp and input directory."""
	image = glob.glob(input_dir + '/SkyImage/' + 'sgptsiskyimageC1.a1.' + time_to_year_month_day(
		time) + '*')[0] + '/' + 'sgptsiskyimageC1.a1.' + time_to_year_month_day(
		time) + '.' + time_to_hour_minute_second(
		time) + '.jpg.' + time + '.jpg'
	return image


def extract_mask_path_from_time(time, input_dir):
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


def simplify_image(timestamp, input_dir, output_dir):
	"""Writes simplified versions of mask to simplemask."""
	img_path = extract_img_path_from_time(timestamp, input_dir)
	img = misc.imread(img_path)
	img = crop_image(img)
	Image.fromarray(img).save(img_save_path(timestamp, output_dir) + 'simpleimage' + timestamp + '.jpg')
	return


def simplify_mask(timestamp, input_dir, output_dir):
	"""Writes simplified versions of mask to simplemask."""
	mask_path = extract_mask_path_from_time(timestamp, input_dir)
	mask = misc.imread(mask_path)
	mask = crop_image(mask)
	if (mask == YELLOW).all(axis=2).any():
		mask[(mask == YELLOW).all(axis=2)] = BLACK
	else:
		mask = remove_white_sun(mask)
	Image.fromarray(mask).save(mask_save_path(timestamp, output_dir) + 'simplemask' + timestamp + '.png')
	return

