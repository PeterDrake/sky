import sys
from config import RAW_DATA_DIR
from utils import *
import imageio
from preprocess import *
from fsc import *
import pandas as pd


def work_on_mask(timestamp, input_dir):
	"""Writes simplified versions of mask to simplemask."""
	mask_path = extract_mask_path_from_time_raw(timestamp, input_dir)
	mask = np.asarray(imageio.imread(mask_path))
	print('mask shape')
	print(mask.shape)
	print('mask == yellow shape')
	print((mask == YELLOW).shape)
	if (mask == YELLOW).all(axis=2).any():
		mask[(mask == YELLOW).all(axis=2)] = BLACK
	else:
		mask = remove_white_sun(mask)
	(y, x), radius = find_center(mask)
	global data
	data.append({'time': timestamp, 'y': y, 'x': x, 'radius': radius})
	return


def preprocess(filename):
	"""Simplifies sky and decision images given a filename containing timestamps and an output_dir to save the
	simplified images."""
	file = open(filename)
	print("Opened {}".format(filename))
	for time in file:
		time = time.replace('\n', '')
		time = time.replace(' ', '')
		work_on_mask(time, RAW_DATA_DIR)
	file.close()
	print("Finished preprocessing sky and decision images in ", filename)


if __name__ == "__main__":
	f = sys.argv[1]
	data = []
	preprocess(f)
	centers = pd.DataFrame(data)
	centers.to_csv('centers.csv')


# SGE_Batch -r "center0" -c "python3 -u center.py typical_data/res/batch0.txt" -P 1
