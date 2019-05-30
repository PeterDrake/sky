"""
This script is intended to be run from preprocess_launch.py, which calls this script and sends it a file. In that
file should be a collection of timestamps separated by line.

This script crops the sky photos and simplifies the decision images in the RAW_DATA_DIR. Simplification entails cropping
and removal of the sun from the sun band.
"""

import sys

from config import RAW_DATA_DIR
from utils import *
import matplotlib.pyplot as plt


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
	img_path = extract_img_path_from_time_raw(timestamp, input_dir)
	img = plt.imread(img_path)
	img = crop_image(img)
	Image.fromarray(img).save(img_save_path(timestamp, output_dir) + 'simpleimage' + timestamp + '.jpg')
	return


def simplify_mask(timestamp, input_dir, output_dir):
	"""Writes simplified versions of mask to simplemask."""
	mask_path = extract_mask_path_from_time_raw(timestamp, input_dir)
	mask = plt.imread(mask_path)
	mask = crop_image(mask)
	if (mask == YELLOW).all(axis=2).any():
		mask[(mask == YELLOW).all(axis=2)] = BLACK
	else:
		mask = remove_white_sun(mask)
	Image.fromarray(mask).save(mask_save_path(timestamp, output_dir) + 'simplemask' + timestamp + '.png')
	return


def preprocess(filename, output_dir):
	"""Simplifies sky and decision images given a filename containing timestamps and an output_dir to save the
	simplified images."""
	file = open(filename)
	print("Opened {}".format(filename))
	for time in file:
		time = time.replace('\n', '')
		time = time.replace(' ', '')
		simplify_mask(time, RAW_DATA_DIR, output_dir)
		simplify_image(time, RAW_DATA_DIR, output_dir)
	file.close()
	print("Finished preprocessing sky and decision images in ", filename)


if __name__ == "__main__":
	f = sys.argv[1]
	OUTPUT_DIR = sys.argv[2]
	preprocess(f, OUTPUT_DIR)
