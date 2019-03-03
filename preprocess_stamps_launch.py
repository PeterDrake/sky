"""
This script should be run after the preprocess_launch.py script has completed its task.

This script creates pickled files for timestamps and creates a constant mask in the OUTPUT_DIR directory. For
sensible results, the decision images should already be simplified.

Recommended to run this script on blt with the command:
SGE_Batch -r "preprocess_stamps" -c "python3 -u preprocess_stamps_launch.py" -P 1
"""

import numpy as np
import os
from PIL import Image
from scipy import misc
from utils import extract_times_from_files_in_directory, separate_data, BLACK, BLUE
from config import TYPICAL_DATA_DIR, TYPICAL_DATA_CSV


def create_constant_mask(color, filename):
	"""Creates a mask where any pixels not always of color are BLUE. Saves it in filename."""
	b_mask = np.full((480, 480, 3), color)
	for dirpath, subdirs, files in os.walk(TYPICAL_DATA_DIR + '/simplemask/'):
		for file in files:
			img = misc.imread(os.path.join(dirpath, file))
			b_mask[(img != color).any(axis=2)] = BLUE
	Image.fromarray(b_mask.astype('uint8')).save(filename)


def setup(train, valid, test):
	times = extract_times_from_files_in_directory(TYPICAL_DATA_DIR + "/res")
	separate_data(times, train, valid, test)
	create_constant_mask(BLACK, TYPICAL_DATA_DIR + '/always_black_mask.png')


if __name__ == "__main__":
	train_stamp_path = TYPICAL_DATA_DIR + '/train.stamps'
	valid_stamp_path = TYPICAL_DATA_DIR + '/valid.stamps'
	test_stamp_path = TYPICAL_DATA_DIR + '/test.stamps'
	setup(train_stamp_path, valid_stamp_path, test_stamp_path)
