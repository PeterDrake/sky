"""
This program can be called after the train_launch.py finishes its task.

This program processes simplified sky images through the trained network to create decision images. Processing is run in
parallel if BLT is set to True, significantly reducing the time needed to process large numbers of sky images. If BLT is
set to False in the config file then processing is sequential.
"""

import os
from config import BLT
from process import process

# Specify the labels that correspond to networks of interest. Ie 'e70-00'
exp_labels = ['e81-00']

# Specify the number of batches to run per network. This allows for tasks to be run in parallel (For BLT).
num_batches_per_network = 1


def launch_process(input_data_csv, job_name, input_dir):
	"""Starts processing tasks."""
	total_length = -1  # This file has a header
	for _ in open(input_data_csv):
		total_length += 1
	batch_length = int(total_length / num_batches_per_network)
	for exp_label in exp_labels:
		for i in range(num_batches_per_network):
			name = job_name + exp_label + '-{:0>2}'.format(i)
			start = batch_length * i
			finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
			if BLT:
				os.system('SGE_Batch -r "{}" -c "python3 -u process.py {} {} {} {} {}" -P 1'.format(name, exp_label, int(start), int(finish), input_dir, input_data_csv))
			else:
				process(exp_label, int(start), int(finish), input_dir, input_data_csv)


if __name__ == "__main__":
	launch_process("dubious_data/shcu_dubious_data.csv", "process-dubious-", "dubious_data")
	launch_process("typical_data/shcu_typical_data.csv", "process-typical-", "typical_data")
