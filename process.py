"""
This is called by process_launch.
Processes sky images into cloud masks. Requires command line arguments for the experiment label, starting index,
and ending index. Experiment label is to specify the directory in which the network is stored WITHIN the results
directory.
"""

import os
import sys

from process_launch import network_output_exists, process_network_masks
from utils import extract_data_from_csv, extract_img_path_from_time

if __name__ == '__main__':
	exp_label = sys.argv[1]  # The experiment number / directory name in results
	start = int(sys.argv[2])  # The starting index of the timestamp in the shcu_good_data.csv file to consider
	finish = int(sys.argv[3])  # Final timestamp to consider
	temp = sorted(list(extract_data_from_csv('shcu_good_data.csv', 'timestamp_utc')))[start:finish]
	times = []
	for t in temp:
		if not network_output_exists(t, exp_label):
			if os.path.isfile(extract_img_path_from_time(t, 'good_data')):
				if os.path.getsize(extract_img_path_from_time(t, 'good_data')) != 0:
					times.append(t)
	masks = process_network_masks(times, exp_label)
