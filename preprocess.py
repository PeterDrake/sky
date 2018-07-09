"""
Opens the file provided by the command line and iterates through it. Expects the file contains timestamps,
one in each row.
"""

import sys

from preprocess_setup_launch import INPUT_DIR, OUTPUT_DIR
from utils import *


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
				if depth_first_search(c, visited, ever_visited, stack):
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


if __name__ == "__main__":
	f = open(sys.argv[1])  # This is the name of the file containing timestamps
	print("Opened {}".format(sys.argv[1]))
	for time in f:
		time = time.replace('\n', '')
		simplify_mask(time, INPUT_DIR, OUTPUT_DIR)
		simplify_image(time, INPUT_DIR, OUTPUT_DIR)
