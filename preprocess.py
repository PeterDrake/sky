import os
from scipy import misc
from PIL import Image
from util import *


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


def simplify_name(filename):
	"""Accepts an arm.gov filename and returns a shorter, simpler version."""
	if "mask" in filename:
		return "simplemask" + filename[-18:]
	if "image" in filename:
		return "simpleimage" + filename[-18:]
	return


def find_unpaired_images(input_dir, timestamps):
	"""Blacklists files for timestamps that do not have both images and masks."""
	for time in extract_timestamp_recur(input_dir):
		mask = 'sgptsicldmaskC1.a1.' + time_to_year_month_day(time) + '.' + time_to_hour_minute_second(
				time) + '.png.' + time + '.png'
		image = 'sgptsiskyimageC1.a1.' + time_to_year_month_day(time) + '.' + time_to_hour_minute_second(
				time) + '.jpg.' + time + '.jpg'
	return

# def count_colors(img):
# 	"""Returns an array of the number of WHITE, BLUE, GRAY, BLACK, and
# 	GREEN pixels in img."""
# 	counts = [(img == color).all(axis=2).sum() for color in COLORS]
# 	return np.array(counts)
#
#
# def create_constant_mask(color, filename):
# 	"""Creates a mask where any pixels not always of color are BLUE. Saves it in
# 	filename."""
# 	b_mask = np.full((480, 480, 3), color)
# 	for file in os.listdir('simplemask/'):
# 		img = misc.imread('simplemask/' + file)
# 		b_mask[(img != color).any(axis=2)] = BLUE
# 	Image.fromarray(b_mask.astype('uint8')).save(filename)

# print(os.listdir())
