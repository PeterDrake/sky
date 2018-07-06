"""
Run this program to launch fsc_analyze.py
Creates and saves plots comparing fsc value from ceilometer, network and TSI for good and bad data (for timestamps
from shcu_good_data.csv or shcu_bad_data.csv)
"""

import os

exp_labels = ['e70-00', 'e70-01', 'e70-02', 'e70-03',
	'e70-04']  # Specify the labels that correspond to networks of interest. Ie 'e70-00'

if __name__ == "__main__":
	for exp_label in exp_labels:
		name = "fsc-compare-" + exp_label
		fsc_path = 'results/' + exp_label + '/fsc.csv'
		os.system('SGE_Batch -r "{}" -c "python3 -u fsc_analyze.py {}" -P 1'.format(name, fsc_path))
