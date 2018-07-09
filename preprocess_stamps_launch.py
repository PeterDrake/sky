"""
This program creates pickled files for timestamps and creates a constant mask in the output directory.
"""

from preprocess_setup_launch import *
from utils import extract_times_from_files_in_directory, separate_data, BLACK

OUTPUT_DIR = "good_data"
RES_DIR = "res"

if __name__ == "__main__":
	times = extract_times_from_files_in_directory(RES_DIR)
	separate_data(times, output_dir=OUTPUT_DIR)
	create_constant_mask(BLACK, OUTPUT_DIR + '/always_black_mask.png')
