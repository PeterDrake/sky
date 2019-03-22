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
import time


def setup(job_name, input_data_csv, output_data_csv):
	name = job_name + EXPERIMENT_LABEL
	if BLT:
		os.system('SGE_Batch -r "{}" -c "python3 -u fsc.py {} {}" -P 1'.format(name, input_data_csv, output_data_csv))
	else:
		fsc(input_data_csv, output_data_csv)


if __name__ == "__main__":
	start = time.clock()
	setup('dubious-fsc-', DUBIOUS_DATA_CSV, 'dubious_fsc.csv')
	setup('typical-fsc-', TYPICAL_DATA_CSV, 'typical_fsc.csv')
	print("Elapsed time: " + str(time.clock() - start) + " seconds")
