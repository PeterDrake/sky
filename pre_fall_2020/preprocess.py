"""
This script is intended to be run from preprocess_launch.py, which calls this script and sends it a file. In that
file should be a collection of timestamps separated by line.

This script crops the sky photos and simplifies the decision images in the RAW_DATA_DIR. Simplification entails
cropping, centering, adding a consistent black border to images, and removal of the sun from the sun band.
"""

from fsc import *
import imageio
from collections import Counter

def remove_green(decision_img):
	"""
	Returns a copy of decision_img with green pixels replaced with the most common nearby color.
	(The TSI puts some green lines in the decision images to indicate regions around the sun and zenith.)
	"""
	result = np.copy(decision_img)
	for i in range(decision_img.shape[0]):
		for j in range(decision_img.shape[0]):
			if np.array_equal(decision_img[i][j], GREEN):
				# This is the size of the starting square size that gets voted on
				radius = 1
				while True:
					window = (decision_img[i - radius:i + radius + 1, j - radius:j + radius + 1])
					counts = Counter()
					for x in range(radius * 2 + 1):
						for y in range(radius * 2 + 1):
							if np.array_equal(window[x][y], WHITE):
								counts[0] += 1
							elif np.array_equal(window[x][y], BLUE):
								counts[1] += 1
							elif np.array_equal(window[x][y], GRAY):
								counts[2] += 1
					if counts:
						break
					else:  # No useful neighboring pixels found; expand the radius and try again
						radius += 1
				color, _ = counts.most_common(1)[0]
				result[i][j] = COLORS[color]
	return result


def remove_white_sun(decision_img, stride=10):
	"""Removes the sun disk from decision_img if it is white. (A yellow sun is easier to remove; that is handled
	directly in simplify_masks.) Stride indicates distance between pixels from which sun searches are started."""
	ever_visited = np.full(decision_img.shape[:2], False, dtype=bool)  # Visited starting from any pixel
	visited = np.full(decision_img.shape[:2], False, dtype=bool)  # Visited in the current depth-first search
	for r in range(0, decision_img.shape[0], stride):
		for c in range(0, decision_img.shape[1], stride):
			if (decision_img[r][c] == WHITE).all():
				stack = [(r, c)]
				visited.fill(False)
				if depth_first_search(decision_img, visited, ever_visited, stack):
					# We found a white region surrounded by black! Paint it black and return the updated image.
					decision_img[visited] = BLACK
					return decision_img
	return decision_img  # No sun found


def depth_first_search(decision_img, visited, ever_visited, stack):
	"""Returns True if there is a connected region including decision_img[r][c] that is all WHITE and surrounded by
	BLACK. Adds all pixels visited to both visited and ever_visited."""
	while stack:  # We use a manual stack because of Python's default limit on recursion depth
		r, c = stack.pop()
		if (decision_img[r][c] == BLACK).all():
			continue
		if visited[r][c]:
			continue
		visited[r][c] = True
		if ever_visited[r][c]:
			return False
		ever_visited[r][c] = True
		if (decision_img[r][c] == GREEN).all() or (decision_img[r][c] == BLUE).all()\
			or (decision_img[r][c] == GRAY).all():
			return False
		# Note that we don't have to worry about going out of the array bounds because all TSI decision images have
		# black outer borders.
		stack.extend(((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
	return True


def center_and_add_border(decision_img, img):
	"""
	Returns new versions of decision_img and img that have been centered, cropped to 480x480, and
	(in img) had a black bordered added via add_border.
	"""
	(center_row, center_column), radius = find_center(decision_img)
	left_buffer = 0
	right_buffer = 0
	top_buffer = 0
	bottom_buffer = 0
	crop_right = False
	crop_left = False
	crop_top = False
	crop_bottom = False
	if center_column <= 239:
		left_buffer = abs(239 - center_column)
		crop_right = True
	else:
		right_buffer = abs(239 - center_column)
		crop_left = True
	if center_row > 319:
		bottom_buffer = abs(319 - center_row)
		crop_top = True
	else:
		top_buffer = abs(319 - center_row)
		crop_bottom = True
	row = np.array([[0, 0, 0] for i in range(480)])
	column = np.array([0, 0, 0])
	for i in range(int(np.ceil(top_buffer))):
		decision_img = np.insert(decision_img, 1, row, axis=0)
		img = np.insert(img, 1, row, axis=0)
	for i in range(int(np.ceil(bottom_buffer))):
		decision_img = np.insert(decision_img, decision_img.shape[0] - 1, row, axis=0)
		img = np.insert(img, img.shape[0]-1, row, axis=0)
	for i in range(int(np.ceil(left_buffer))):
		decision_img = np.insert(decision_img, 1, column, axis=1)
		img = np.insert(img, 1, column, axis=1)
	for i in range(int(np.ceil(right_buffer))):
		decision_img = np.insert(decision_img, decision_img.shape[1] - 1, column, axis=1)
		img = np.insert(img, img.shape[1]-1, column, axis=1)
	if crop_right:
		right_trim = int(np.ceil(decision_img.shape[1] - 480))  # TODO Is this not a constant?
		img = np.delete(img, slice((img.shape[1] - right_trim - 1), img.shape[1] - 1), axis=1)
		decision_img =\
			np.delete(decision_img, slice((decision_img.shape[1] - right_trim - 1), decision_img.shape[1] - 1), axis=1)
	if crop_left:
		left_trim = int(np.floor(decision_img.shape[1] - 480))
		img = np.delete(img, slice(0, left_trim), axis=1)
		decision_img = np.delete(decision_img, slice(0, left_trim), axis=1)
	if crop_top:
		img = np.delete(img, slice(img.shape[0] - 80 - 1, img.shape[0] - 1), axis=0)
		decision_img = np.delete(decision_img, slice(decision_img.shape[0] - 80 - 1, decision_img.shape[0] - 1), axis=0)
		top_trim = int(np.ceil(decision_img.shape[0] - 480))
		img = np.delete(img, slice(0, top_trim), axis=0)
		decision_img = np.delete(decision_img, slice(0, top_trim), axis=0)
	if crop_bottom:
		img = np.delete(img, slice(0, 80), axis=0)
		decision_img = np.delete(decision_img, slice(0, 80), axis=0)
		bottom_trim = int(np.floor(decision_img.shape[0] - 480))
		img = np.delete(img, slice((img.shape[0] - bottom_trim - 1), img.shape[0] - 1), axis=0)
		decision_img =\
			np.delete(decision_img, slice((decision_img.shape[0] - bottom_trim - 1), decision_img.shape[0] - 1), axis=0)
	img = add_border(decision_img, img, radius)
	return decision_img, img


def add_border(decision_img, img, radius):
	"""
	Modifies img to mark black any pixels that are both black in decision_img and at least radius pixels away from
	the center. This is important so that the network won't have to learn to distinguish the white TSI hardware
	housing from clouds.
	
	Returns the revised version of img.
	"""
	for i in range(decision_img.shape[0]):
		for j in range(decision_img.shape[1]):
			a = (i - 239) ** 2
			b = (j - 239) ** 2
			if np.array_equal(decision_img[i][j], BLACK) and a + b > (radius ** 2):
				img[i][j] = [0, 0, 0]
	return img


def simplify(timestamp, input_dir, output_dir):
	"""
	Finds an image and a decision image in input_dir, then writes corresponding simplified versions to output_dir.
	Simplification means removing the sun, centering, adding a consistent black border, and removing the TSI's
	green lines.
	"""
	decision_img_path = extract_mask_path_from_time_raw(timestamp, input_dir)
	decision_img = np.asarray(imageio.imread(decision_img_path, pilmode="RGB"))
	img_path = extract_img_path_from_time_raw(timestamp, input_dir)
	img = np.asarray(imageio.imread(img_path, pilmode="RGB"))
	if (decision_img == YELLOW).all(axis=2).any():
		decision_img[(decision_img == YELLOW).all(axis=2)] = BLACK
	else:
		decision_img = remove_white_sun(decision_img)
	decision_img, img = center_and_add_border(decision_img, img)
	decision_img = remove_green(decision_img)
	Image.fromarray(decision_img).save(mask_save_path(timestamp, output_dir) + 'simplemask' + timestamp + '.png')
	Image.fromarray(img).save(img_save_path(timestamp, output_dir) + 'simpleimage' + timestamp + '.jpg')
	return


def preprocess(filename, output_dir):
	"""Simplifies sky and decision images given a filename containing timestamps and an output_dir to save the
	simplified images."""
	with open(filename, 'r') as file:
		print("Opened {}".format(filename))
		for time in file:
			time = time.replace('\n', '')
			time = time.replace(' ', '')
			simplify(time, RAW_DATA_DIR, output_dir)
	print("Finished preprocessing sky and decision images in ", filename)


if __name__ == "__main__":
	# Command-line arguments are source directory and destination directory
	preprocess(sys.argv[1], sys.argv[2])