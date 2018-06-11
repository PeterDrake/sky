import glob

import numpy as np

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
	blacklist = set()
	for time in timestamps:
		mask = input_dir + '/CloudMask/' + 'sgptsicldmaskC1.a1.' + time_to_year_month_day(
				time) + '/' + 'sgptsicldmaskC1.a1.' + time_to_year_month_day(time) + '.' + time_to_hour_minute_second(
				time) + '.png.' + time + '.png'
		image = glob.glob(input_dir + '/SkyImage/' + 'sgptsiskyimageC1.a1.' + time_to_year_month_day(
				time) + '*')[0] + '/' + 'sgptsiskyimageC1.a1.' + time_to_year_month_day(
				time) + '.' + time_to_hour_minute_second(
				time) + '.jpg.' + time + '.jpg'
		if not os.path.isfile(mask) or not os.path.isfile(image):
			blacklist.add(time)
		elif os.path.getsize(mask) == 0 or os.path.getsize(image) == 0:
			blacklist.add(time)
	return blacklist


def crop_image(img):
	"""Expect img to be a numpy array of size 640 x 480. Returns a version of img cropped down to 480 x 480.
	Axis = 0 is the vertical axis (i.e. rows) from which the first and last 80 pixels are deleted."""
	return np.delete(img, np.concatenate((np.arange(80), np.arange(80) + 560)), axis=0)
