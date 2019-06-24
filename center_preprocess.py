"""
This script is intended to be run from preprocess_launch.py, which calls this script and sends it a file. In that
file should be a collection of timestamps separated by line.

This script crops the sky photos and simplifies the decision images in the RAW_DATA_DIR. Simplification entails cropping
and removal of the sun from the sun band.
"""

import sys

from config import RAW_DATA_DIR
from utils import *
from fsc import *
import imageio


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


def center_and_add_border(mask, img):
	(y, x), radius = find_center(mask)
	left_buffer = 0
	right_buffer = 0
	top_buffer = 0
	bottom_buffer = 0
	crop_right = False
	crop_left = False
	crop_top = False
	crop_bottom = False
	if x <= 239:
		left_buffer = abs(239 - x)
		crop_right = True
	if x > 239:
		right_buffer = abs(239 - x)
		crop_left = True
	if y > 319:
		bottom_buffer = abs(319 - y)
		crop_top = True
	if y <= 319:
		top_buffer = abs(319 - y)
		crop_bottom = True
	row = np.array([[0, 0, 0] for i in range(480)])
	column = np.array([0, 0, 0])
	for i in range(int(np.ceil(top_buffer))):
		mask = np.insert(mask, 1, row, axis=0)
		img = np.insert(img, 1, row, axis=0)
	for i in range(int(np.ceil(bottom_buffer))):
		mask = np.insert(mask, mask.shape[0]-1, row, axis=0)
		img = np.insert(img, img.shape[0]-1, row, axis=0)
	for i in range(int(np.ceil(left_buffer))):
		mask = np.insert(mask, 1, column, axis=1)
		img = np.insert(img, 1, column, axis=1)
	for i in range(int(np.ceil(right_buffer))):
		mask = np.insert(mask, mask.shape[1]-1, column, axis=1)
		img = np.insert(img, img.shape[1]-1, column, axis=1)
	if crop_right:
		right_trim = int(np.ceil(mask.shape[1] - 480))
		img = np.delete(img, slice((img.shape[1] - right_trim - 1), img.shape[1] - 1), axis=1)
		mask = np.delete(mask, slice((mask.shape[1] - right_trim - 1), mask.shape[1] - 1), axis=1)
	if crop_left:
		left_trim = int(np.floor(mask.shape[1] - 480))
		img = np.delete(img, slice(0, left_trim), axis=1)
		mask = np.delete(mask, slice(0, left_trim), axis=1)
	if crop_top:
		img = np.delete(img, slice(img.shape[0] - 80 - 1, img.shape[0] - 1), axis=0)
		mask = np.delete(mask, slice(mask.shape[0] - 80 - 1, mask.shape[0] - 1), axis=0)
		top_trim = int(np.ceil(mask.shape[0] - 480))
		img = np.delete(img, slice(0, top_trim), axis=0)
		mask = np.delete(mask, slice(0, top_trim), axis=0)
	if crop_bottom:
		img = np.delete(img, slice(0, 80), axis=0)
		mask = np.delete(mask, slice(0, 80), axis=0)
		bottom_trim = int(np.floor(mask.shape[0] - 480))
		img = np.delete(img, slice((img.shape[0] - bottom_trim - 1), img.shape[0] - 1), axis=0)
		mask = np.delete(mask, slice((mask.shape[0] - bottom_trim - 1), mask.shape[0] - 1), axis=0)
	img = add_border(mask, img, radius)
	return mask, img


def add_border(mask, img, radius):
	for i in range(mask.shape[0]):
		for j in range(mask.shape[1]):
			a = (i - 239) ** 2
			b = (j - 239) ** 2
			if np.array_equal(mask[i][j], np.array([0, 0, 0])) and a + b > (radius ** 2):
				img[i][j] = [0, 0, 0]
	return img


def simplify(timestamp, input_dir, output_dir):
	mask_path = extract_mask_path_from_time_raw(timestamp, input_dir)
	mask = np.asarray(imageio.imread(mask_path, pilmode="RGB"))
	img_path = extract_img_path_from_time_raw(timestamp, input_dir)
	img = np.asarray(imageio.imread(img_path, pilmode="RGB"))
	if (mask == YELLOW).all(axis=2).any():
		mask[(mask == YELLOW).all(axis=2)] = BLACK
	else:
		mask = remove_white_sun(mask)
	mask, img = center_and_add_border(mask, img)
	Image.fromarray(mask).save(mask_save_path(timestamp, output_dir) + 'simplemask' + timestamp + '.png')
	Image.fromarray(img).save(img_save_path(timestamp, output_dir) + 'simpleimage' + timestamp + '.jpg')
	return


def prac_simplify(mask, img):
	if (mask == YELLOW).all(axis=2).any():
		mask[(mask == YELLOW).all(axis=2)] = BLACK
	else:
		mask = remove_white_sun(mask)
	mask, img = center_and_add_border(mask, img)
	return mask, img


def preprocess(filename, output_dir):
	"""Simplifies sky and decision images given a filename containing timestamps and an output_dir to save the
	simplified images."""
	file = open(filename)
	print("Opened {}".format(filename))
	for time in file:
		time = time.replace('\n', '')
		time = time.replace(' ', '')
		simplify(time, RAW_DATA_DIR, output_dir)
	file.close()
	print("Finished preprocessing sky and decision images in ", filename)


if __name__ == "__main__":
	f = sys.argv[1]
	OUTPUT_DIR = sys.argv[2]
	preprocess(f, OUTPUT_DIR)