"""
Opens shcu_good_times.csv and looks for missing or empty files on the BLT cluster in the specified input directory.
For each type of missing or empty file, a text file is created that contains a list of timestamps pertaining to that
type of bad file.
"""

import os
from utils import extract_img_path_from_time_old, extract_mask_path_from_time_old, extract_data_from_csv, \
	write_list_to_file

# The directory on BLT to the directory containing folders for masks and images
INPUT_DIR = '/home/users/jkleiss/TSI_C1'


def why_bad_files(timestamps, input_dir=INPUT_DIR):
	"""Returns four sets that self describe why a file in the given list is bad. A file in the input directory is bad
	if it is missing or empty. This method checks those conditions for both masks and images."""
	missing_mask, empty_mask, missing_image, empty_image = set(), set(), set(), set()
	for stamp in timestamps:
		mask = extract_mask_path_from_time_old(stamp, input_dir)
		image = extract_img_path_from_time_old(stamp, input_dir)
		if os.path.isfile(mask):
			missing_mask.add(stamp)
		elif os.path.getsize(mask) == 0:
			empty_mask.add(stamp)
		if not os.path.isfile(image):
			missing_image.add(stamp)
		elif os.path.getsize(image) == 0:
			empty_image.add(stamp)
	return missing_image, empty_image, missing_mask, empty_mask


if __name__ == '__main__':
	good_times = extract_data_from_csv("shcu_good_data.csv", "timestamp_utc")

	print("there are {} times from the csv file".format(len(good_times)))
	missing_images, empty_images, missing_masks, empty_masks = why_bad_files(good_times)

	print("Writing to missing_images.txt. There are {} missing images".format(len(missing_images)))
	if missing_images:
		write_list_to_file(missing_images, 'missing_images.txt')

	print("Writing to empty_images.txt. There are {} empty images".format(len(empty_images)))
	if empty_images:
		write_list_to_file(empty_images, 'empty_images.txt')

	print("Writing to 'missing_masks.txt'. There are {} missing masks.".format(len(missing_masks)))
	if missing_masks:
		write_list_to_file(missing_masks, 'missing_masks.txt')

	print("Writing to 'empty_masks.txt'. There are {} empty masks.".format(len(empty_masks)))
	if empty_masks:
		write_list_to_file(empty_masks, 'empty_masks.txt')
