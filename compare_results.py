from preprocess import *

# Constants for input and output locations
INPUT_DIR = '/home/users/jkleiss/TSI_C1'
OUTPUT_DIR = '/home/users/msl/new_data'


def count_expected():
	good_times = extract_times_from_csv()
	blacklist = find_unpaired_images(good_times, INPUT_DIR)
	times = good_times - blacklist
	print("This is the number of timestamps for which we should simplify: ", len(times))
	return len(times)


def count_blt():
	print("This is the number of files in Jessica's dir: ",
	      len(extract_all_times(INPUT_DIR, ['/SkyImage', '/CloudMask'])))
	return len(extract_all_times(INPUT_DIR, ['/SkyImage', '/CloudMask']))


def count_actual():
	print("This is the number of timestamps for which we simplify: ",
	      len(extract_all_times(OUTPUT_DIR, ['/simpleimage', '/simplemask'])))
	return len(extract_all_times(OUTPUT_DIR, ['/simpleimage', '/simplemask']))


if __name__ == '__main__':
	# expected = count_expected()
	# actual = count_actual()
	# if expected == actual:
	# 	print('numbers match! Actual: ' + actual + 'Expected: ' + expected)
	# else:
	# 	print('numbers dont match. Actual: ' + actual + 'Expected: ' + expected)
	count_blt()
