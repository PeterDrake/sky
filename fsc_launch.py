"""
Run this program to create a csv file for each network. Each csv contains the timestamp, fsc_z, fsc_thn_z,
and fsc_opq_z for all of the times that have been processed by the network.
Run this only after process_launch.py has finished processing all of the masks desired.
"""

import os

if __name__ == "__main__":
	exp_labels = ['e72-00', 'e72-01', 'e72-02']

	for exp_label in exp_labels:
		name = "fsc-csv-" + exp_label
		os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {}" -P 1'.format(name, exp_label))