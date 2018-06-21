import os

exp_labels = ['e70-00', 'e70-01', 'e70-02', 'e70-03', 'e70-04']

for exp_label in exp_labels:
	name = "fsc_net-" + exp_label
	os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {}" -P 1'.format(name, exp_label))
