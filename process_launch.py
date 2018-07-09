"""
Call this program after completing all preprocess launch tasks. This method goes through all cropped sky images and
produces the network output mask for each. Breaks up tasks into many smaller batches to improve speed. Specify the
number of batches per network to increase the number of batches created & increase speed. Make sure that the number
of batches times the number of batches per network is small enough so that BLT can fit all of the jobs.
"""

import os

# Specify the directory where the sky images are stored: ex: good_data
INPUT_DIR = "good_data"

# Specify the location of the csv file that contains desired timestamp_utc information.
input_csv = "shcu_good_data.csv"

# Specify the labels that correspond to networks of interest. Ie 'e70-00'
exp_labels = ['e73-00', 'e73-01']

# Specify the number of batches to run per network. This helps parallelize the processing task.
num_batches_per_network = 5

if __name__ == "__main__":
	num_batches = len(exp_labels)

	total_length = -1  # This file has a header
	for line in open(input_csv):
		total_length += 1

	batch_length = int(total_length / num_batches_per_network)

	for exp_label in exp_labels:
		for i in range(num_batches_per_network):
			name = "good-net-" + exp_label + "-" + str(i)
			start = batch_length * i
			finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
			os.system('SGE_Batch -r "{}" -c "python3 -u process.py {} {} {}" -P 1'.format(name, exp_label, int(start),
					int(finish)))
