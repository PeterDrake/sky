from preprocess import *

# Constants for input and output locations
INPUT_DIR = '/home/users/jkleiss/TSI_C1'
OUTPUT_DIR = 'good_data'


def why_bad_images(timestamps, input_dir=INPUT_DIR):
	"""Blacklists files for timestamps that do not have both images and masks."""
	bad_mask = set()
	missing_image = set()
	empty_image = set()
	for time in timestamps:
		mask = extract_mask_path_from_time(time, input_dir)
		image = extract_img_path_from_time(time, input_dir)
		if not os.path.isfile(mask) or os.path.getsize(mask) == 0:
			bad_mask.add(time)
		if not os.path.isfile(image):
			missing_image.add(time)
		if os.path.getsize(image) == 0:
			empty_image.add(time)
	return bad_image.union(bad_mask), bad_image, bad_mask


def count_expected():
	good_times = extract_times_from_csv()
	blacklist, bad_image, bad_mask = why_bad_images(good_times, INPUT_DIR)
	times = good_times - blacklist
	return


def count_blt():
	print("This is the number of files in Jessica's dir: ",
			len(extract_all_times(INPUT_DIR, ['/SkyImage', '/CloudMask'])))
	return len(extract_all_times(INPUT_DIR, ['/SkyImage', '/CloudMask']))


def count_actual():
	print("This is the number of timestamps for which we simplify: ",
			len(extract_all_times(OUTPUT_DIR, ['/simpleimage', '/simplemask'])))
	return len(extract_all_times(OUTPUT_DIR, ['/simpleimage', '/simplemask']))


if __name__ == '__main__':
	good_times = extract_times_from_csv()
	blacklist, bad_images, bad_masks = why_bad_images(good_times)

	print("Writing to bad_image_times.txt! There are {} timestamps corresponding to images that do not work "
	      "well.".format(len(bad_images)))
	with open("bad_image_times.txt", 'w') as img_file:
		img_file.writelines("%s\n" % img for img in bad_images)

	print("Writing to bad_mask_times.txt! There are {} timestamps corresponding to masks that do not work "
	      "well.".format(len(bad_masks)))
	with open("bad_mask_times.txt", 'w') as mask_file:
		mask_file.writelines("%s\n" % mask for mask in bad_masks)

	print("Writing to bad_times.txt! There are {} timestamps corresponding to masks or images that do not work "
	      "well.".format(len(blacklist)))
	with open("bad_times.txt", 'w') as bad_file:
		bad_file.writelines("%s\n" % time for time in blacklist)
