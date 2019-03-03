"""
This script is intended to be run once the process_launch.py script has completed its task.

This script launches the fsc.py script, which evaluates the fractional sky cover for every decision image in the
network's mask directory. The fsc.py script saves its results in the OUTPUT_DATA_CSV file in the network's directory.
EX: head results/e70-00/fsc.csv --lines=2
	timestamp_utc,fsc_z,fsc_thn_z,fsc_opq_z
	20120501170000,0.39586249209118624,0.13311731886419848,0.26274517322698776

This script also defines the INPUT_DATA_CSV file, which should contain a timestamp_utc header and timestamps that
correspond to the decision images you wish to use in fractional sky cover calculations.
EX: 'typical_data/shcu_typical_data.csv'
"""

import os
from config import *
from fsc import fsc

# Set the experiment labels to match the network(s) you'd like to evaluate fractional sky cover tasks with
# Note: this is not used to open the network, but rather to look through its processed decision images
EXP_LABELS = ['e82-00']


def setup(job_name, input_data_csv, output_data_csv):
	for exp_label in EXP_LABELS:
		name = job_name + exp_label
		if BLT:
			os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {} {} {}" -P 1'.format(name, exp_label, input_data_csv, output_data_csv))
		else:
			fsc(exp_label, input_data_csv, output_data_csv)


if __name__ == "__main__":
	setup('dubious-fsc-', DUBIOUS_DATA_CSV, 'dubious_fsc.csv')
	setup('typical-fsc-', TYPICAL_DATA_CSV, 'typical_fsc.csv')
