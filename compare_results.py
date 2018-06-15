from preprocess import *

# Constants for input and output locations
INPUT_DIR = '/home/users/jkleiss/TSI_C1'
OUTPUT_DIR = 'good_data'


def why_bad_images(timestamps, input_dir=INPUT_DIR):
	"""Blacklists files for timestamps that do not have both images and masks."""
	missing_mask = set()
	empty_mask = set()
	missing_image = set()
	empty_image = set()
	for time in timestamps:
		mask = extract_mask_path_from_time(time, input_dir)
		image = extract_img_path_from_time(time, input_dir)
		if not os.path.isfile(mask):
			missing_mask.add(time)
		if os.path.getsize(mask) == 0:
			empty_mask.add(time)
		if not os.path.isfile(image):
			missing_image.add(time)
		if os.path.getsize(image) == 0:
			empty_image.add(time)
	return missing_image, empty_image, missing_mask, empty_mask


def count_expected():
	"""Counts the number of unique timestamps we expect to simplify."""
	good_times = extract_times_from_csv("shcu_good_data.csv", "timestamp_utc")
	blacklist, bad_image, bad_mask = why_bad_images(good_times, INPUT_DIR)
	times = good_times - blacklist
	return len(times)


def count_blt():
	"""Counts the number of unique timestamps in the BLT input directory."""
	num_times = len(extract_all_times(INPUT_DIR, ['/SkyImage', '/CloudMask']))
	print("This is the number of files in Jessica's dir: ", num_times)
	return num_times


def count_actual():
	"""Counts the number of unique timestamps in the BLT target directory."""
	num_times = len(extract_all_times(OUTPUT_DIR, ['/simpleimage', '/simplemask']))
	print("This is the number of timestamps for which we simplify: ", num_times)
	return num_times


if __name__ == '__main__':
	good_times = extract_times_from_csv("shcu_good_data.csv", "timestamp_utc")
	missing_images, empty_images, missing_masks, empty_masks = why_bad_images(good_times)

	print("Writing to missing_images.txt. There are {} missing images".format(missing_images))
	with open('missing_images.txt', 'wb') as file:
		for time in missing_images:
			file.write(time + '\n')

	print("Writing to empty_images.txt. There are {} empty images".format(empty_images))
	with open('empty_images.txt', 'wb') as file:
		for time in empty_images:
			file.write(time + '\n')

	print("Writing to 'missing_masks.txt'. There are {} missing masks.".format(len(missing_masks)))
	with open('missing_masks.txt', 'wb') as file:
		for time in missing_masks:
			file.write(time + '\n')

	print("Writing to 'empty_masks.txt'. There are {} empty masks.".format(len(empty_masks)))
	with open('empty_masks.txt', 'wb') as file:
		for time in empty_masks:
			file.write(time + '\n')
