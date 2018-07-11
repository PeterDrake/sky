"""
This script should be run after the preprocess_launch.py script has completed its task.

This script creates pickled files for timestamps and creates a constant mask in the OUTPUT_DIR directory. For
sensible results, the decision images should already be simplified.

Recommended to run this script on blt with the command:
SGE_Batch -r "preprocess_stamps" -c "python3 -u preprocess_stamps_launch.py" -P 1
"""

import os
import numpy as np
from PIL import Image
from scipy import misc

from preprocess_setup_launch import OUTPUT_DIR, RES_DIR
from utils import extract_times_from_files_in_directory, separate_data, BLACK, BLUE

# Set the names of the training, validation, and testing timestamp files.
TRAIN_STAMP_PATH = 'train.stamps'
VALID_STAMP_PATH = 'valid.stamps'
TEST_STAMP_PATH = 'test.stamps'


def create_constant_mask(color, filename):
	"""Creates a mask where any pixels not always of color are BLUE. Saves it in filename."""
	b_mask = np.full((480, 480, 3), color)
	for dirpath, subdirs, files in os.walk(OUTPUT_DIR + '/simplemask/'):
		for file in files:
			img = misc.imread(os.path.join(dirpath, file))
			b_mask[(img != color).any(axis=2)] = BLUE
	Image.fromarray(b_mask.astype('uint8')).save(OUTPUT_DIR + '/' + filename)


if __name__ == "__main__":
	times = extract_times_from_files_in_directory(RES_DIR)
	separate_data(times, OUTPUT_DIR, TRAIN_STAMP_PATH, VALID_STAMP_PATH, TEST_STAMP_PATH)
	create_constant_mask(BLACK, OUTPUT_DIR + '/always_black_mask.png')
