from preprocess import *
from collections import Counter
import numpy_indexed as npi


def remove_green(mask):

	for i in range(480):
		for j in range(480):
			choices = []
			if np.array_equal(mask[i][j], GREEN):
				for r in range(1, 5):
					if not np.array_equal(mask[i][j - r], GREEN) and not np.array_equal(mask[i][j - r], BLACK):
						choices.append(mask[i][j - r])
					if not np.array_equal(mask[i][j + r], GREEN) and not np.array_equal(mask[i][j + r], BLACK):
						choices.append(mask[i][j + r])
					if not np.array_equal(mask[i - r][j], GREEN) and not np.array_equal(mask[i - r][j], BLACK):
						choices.append(mask[i - r][j])
					if not np.array_equal(mask[i + r][j], GREEN) and not np.array_equal(mask[i + r][j], BLACK):
						choices.append(mask[i + r][j])
					if len(choices) != 0:
						break
				np.array(choices)
				row = npi.mode(choices)
				mask[i][j] = row

	return mask


def remove_green_v2(mask):

	new_mask = np.copy(mask)

	for i in range(480):
		for j in range(480):
			choices = []
			if np.array_equal(mask[i][j], GREEN):
				for r in range(1, 5):
					if not np.array_equal(mask[i][j - r], GREEN) and not np.array_equal(mask[i][j - r], BLACK):
						choices.append(mask[i][j - r])
					if not np.array_equal(mask[i][j + r], GREEN) and not np.array_equal(mask[i][j + r], BLACK):
						choices.append(mask[i][j + r])
					if not np.array_equal(mask[i - r][j], GREEN) and not np.array_equal(mask[i - r][j], BLACK):
						choices.append(mask[i - r][j])
					if not np.array_equal(mask[i + r][j], GREEN) and not np.array_equal(mask[i + r][j], BLACK):
						choices.append(mask[i + r][j])
					if len(choices) != 0:
						break
				np.array(choices)
				row = npi.mode(choices)
				new_mask[i][j] = row

	return new_mask


def new_remove_green(mask):

	new_mask = np.copy(mask)

	for i in range(mask.shape[0]):
		for j in range(mask.shape[0]):
			if np.array_equal(mask[i][j], GREEN):
				# This is the size of the starting square size that gets voted on
				radius = 1

				while True:

					window = (mask[i - radius:i + radius + 1, j - radius:j + radius + 1])
					choices = Counter()
					for x in range(radius * 2 + 1):
						for y in range(radius * 2 + 1):
							if np.array_equal(window[x][y], BLUE):
								choices['BLUE'] += 1
							elif np.array_equal(window[x][y], GRAY):
								choices['GRAY'] += 1
							elif np.array_equal(window[x][y], WHITE):
								choices['WHITE'] += 1
					if choices:
						break
					else:
						radius += 1

				color, _ = choices.most_common(1)[0]
				new_mask[i][j] = eval(color)

	return new_mask


if __name__ == '__main__':
	m = np.asarray(imageio.imread('typical_data/green_mask_test.png', pilmode="RGB"))
	imageio.imwrite('typical_data/green_mask_results_v3.png', new_remove_green(m))
	imageio.imwrite('typical_data/green_mask_results_v2.png', remove_green_v2(m))
	imageio.imwrite('typical_data/green_mask_results_v1.png', remove_green(m))
