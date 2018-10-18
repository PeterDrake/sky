"""
This script is intended to be run once the process_launch.py script has completed its task.

This script launches the fsc.py script, which evaluates the fractional sky cover for every decision image in the
network's mask directory. The fsc.py script saves its results in the OUTPUT_DATA_CSV file in the network's directory.
EX: head results/e70-00/fsc.csv --lines=2
	timestamp_utc,fsc_z,fsc_thn_z,fsc_opq_z
	20120501170000,0.39586249209118624,0.13311731886419848,0.26274517322698776

This script also defines the INPUT_DATA_CSV file, which should contain a timestamp_utc header and timestamps that
correspond to the decision images you wish to use in fractional sky cover calculations.
EX: 'good_data/shcu_good_data.csv'
"""

import os

# Set the experiment labels to match the network(s) you'd like to evaluate fractional sky cover tasks with
# Note: this is not used to open the network, but rather to look through its processed decision images
EXP_LABELS = ['e77-00']

# Set the input and output csv files to match the file containing timestamps you would like to use.
INPUT_DATA_CSV = 'bad_data/shcu_bad_data.csv'
OUTPUT_DATA_CSV = 'bad_fsc.csv'  # Either good_fsc.csv or bad_fsc.csv for summer 2018
JOB_NAME = 'bad-fsc-'

if __name__ == "__main__":
	for exp_label in EXP_LABELS:
		name = JOB_NAME + exp_label
		os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {}" -P 1'.format(name, exp_label))
