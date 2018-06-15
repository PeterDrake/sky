"""
Opens the file provided by the command line and iterates through it. Expects the file contains timestamps,
one in each row.
"""

import sys

from preprocess import simplify_image, simplify_mask


def batch_process():
	f = open(sys.argv[1])  # This is the name of the file containing timestamps
	print("Opened {}".format(sys.argv[1]))
	for time in f:
		time = time.replace('\n', '')
		simplify_mask(time)
		simplify_image(time)


if __name__ == "__main__":
	batch_process()