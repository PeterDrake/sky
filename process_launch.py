"""
This program can be called after the train_launch.py finishes its task.

This method goes through all cropped sky images and
produces the network output mask for each. Breaks up tasks into many smaller batches to improve speed. Specify the
number of batches per network to increase the number of batches created & increase speed. Make sure that the number
of batches times the number of batches per network is small enough so that BLT can fit all of the jobs.
"""

import os
from config import BLT
# Specify the directory where the sky images are stored: ex: typical_data
#INPUT_DIR = "dubious_data"

# Specify the location of the csv file that contains desired timestamp_utc information.
#INPUT_DATA_CSV = "dubious_data/shcu_dubious_data.csv"

# Specify the base of the job id
#JOB_NAME = "process-dubious-"

# Specify the labels that correspond to networks of interest. Ie 'e70-00'
exp_labels = ['e81-00']

# Specify the number of batches to run per network. This helps parallelize the processing task (For BLT).
num_batches_per_network = 1


def process_BLT(INPUT_DATA_CSV, JOB_NAME,INPUT_DIR):
	""" Processing for BLT. """
	num_batches = len(exp_labels)
	total_length = -1  # This file has a header
	for line in open(INPUT_DATA_CSV):
		total_length += 1
	batch_length = int(total_length / num_batches_per_network)
	for exp_label in exp_labels:
		for i in range(num_batches_per_network):
			name = JOB_NAME + exp_label + '-{:0>2}'.format(i)
			start = batch_length * i
			finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
			os.system('SGE_Batch -r "{}" -c "python3 -u process.py {} {} {} {} {}" -P 1'.format(name, exp_label, int(start), int(finish), INPUT_DIR, INPUT_DATA_CSV))

def process_local(INPUT_DATA_CSV, JOB_NAME,INPUT_DIR):
	""" Processing for BLT. """
	num_batches = len(exp_labels)
	total_length = -1  # This file has a header
	for line in open(INPUT_DATA_CSV):
		total_length += 1
	batch_length = int(total_length / num_batches_per_network)
	for exp_label in exp_labels:
		name = JOB_NAME + exp_label + '-{:0>2}'
		start = 0
		finish = total_length
		os.system('SGE_Batch -r "{}" -c "python3 -u process.py {} {} {} {} {}" -P 1'.format(name, exp_label, int(start), int(finish), INPUT_DIR, INPUT_DATA_CSV))


if __name__ == "__main__":
	if BLT:
		process_BLT("dubious_data/shcu_dubious_data.csv", "process-dubious-", "dubious_data")
		process_BLT("typical_data/shcu_typical_data.csv", "process-typical-", "typical_data")
	else:
		process_local("dubious_data/shcu_dubious_data.csv", "process-dubious-", "dubious_data")
		process_local("typical_data/shcu_typical_data.csv", "process-typical-", "typical_data")