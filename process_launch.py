"""
Call this program after completing all preprocess launch tasks. This method goes through all cropped sky images and
produces the network output mask for each. Breaks up tasks into many smaller batches to improve speed. Specify the
number of batches per network to increase the number of batches created & increase speed. Make sure that the number
of batches times the number of batches per network is small enough so that BLT can fit all of the jobs.
"""

import os

exp_labels = ['e72-00', 'e72-01', 'e72-02']  # Specify the labels that correspond to networks of interest. Ie 'e70-00'

if __name__ == "__main__":
	num_batches = len(exp_labels)
	num_batches_per_network = 10

	total_length = -1  # This file has a header
	for line in open('shcu_good_data.csv'):
		total_length += 1

	batch_length = int(total_length / num_batches_per_network)

	for exp_label in exp_labels:
		for i in range(num_batches_per_network):
			name = "net-" + exp_label + "-" + str(i)
			start = batch_length * i
			finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
			os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {} {} {}" -P 1'.format(name, exp_label, int(start),
					int(finish)))
