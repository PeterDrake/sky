"""
This script should be run after the preprocess_launch.py script has completed its task.

This script creates pickled files for timestamps and creates a constant mask in the OUTPUT_DIR directory. For
sensible results, the decision images should already be simplified.

Recommended to run this script on blt with the command:
SGE_Batch -r "preprocess_stamps" -c "python3 -u preprocess_stamps_launch.py" -P 1
"""

from preprocess_setup_launch import OUTPUT_DIR, RES_DIR, create_constant_mask
from utils import extract_times_from_files_in_directory, separate_data, BLACK

if __name__ == "__main__":
	times = extract_times_from_files_in_directory(RES_DIR)
	separate_data(times, OUTPUT_DIR)
	create_constant_mask(BLACK, OUTPUT_DIR + '/always_black_mask.png')
