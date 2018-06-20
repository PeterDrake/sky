from util import extract_data_from_csv
import os

exp_labels = ['e70-00', 'e70-01', 'e70-02', 'e70-03', 'e70-04']

num_batches = len(exp_labels)
num_batches_per_network = 1

total_length = len(extract_data_from_csv('shcu_good_data.csv', 'timestamp_utc'))
batch_length = total_length / num_batches_per_network

for exp_label in exp_labels:
	for i in range(num_batches_per_network):
		name = None
		start = batch_length * i
		finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
		os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {} {} {}" -P 1'.format(name, exp_label, start, finish))
