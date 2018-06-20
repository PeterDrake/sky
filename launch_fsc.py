import os

exp_labels = ['e70-00', 'e70-01', 'e70-02', 'e70-03', 'e70-04']

num_batches = len(exp_labels)
num_batches_per_network = 1

total_length = -1  # This file has a header
for line in open('shcu_good_data.csv'):
	total_length += 1

batch_length = total_length / num_batches_per_network

for exp_label in exp_labels:
	for i in range(num_batches_per_network):
		name = exp_label + "-" + str(i)
		start = batch_length * i
		finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
		os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {} {} {}" -P 1'.format(name, exp_label, start, finish))
