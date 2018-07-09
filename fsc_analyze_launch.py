"""
This script is intended to be run after the fsc_launch.py script has completed its task.

Plots a comparison between network and the TSI measurements of fractional sky cover. Also compares both sources to
the Laser Ceilometer.

This file is typically run from fsc_analyze_launch.py, but can be run from the command line with an argument for the
experiment label.
EX: python3 fsc_analyze.py e70-00

This script requires four files: 'shcu_good_data.csv', 'shcu_bad_data.csv', 'fsc.csv', and 'bad_fsc.csv'.
* The 'shcu' files should be located in the same directory as this file.
* The 'fsc' files should be located in the results/exp_label/ directory. EX: results/e70-00/fsc.csv

This script creates two plots and saves them as 'good_tsi_arscl_fsc.png' and 'compare_tsi_network_fsc.png' in the
results/exp_label/ directory.
"""

import os
from fsc_launch import EXP_LABELS

if __name__ == "__main__":
	for exp_label in EXP_LABELS:
		name = "fsc-compare-" + exp_label
		os.system('SGE_Batch -r "{}" -c "python3 -u fsc_analyze.py {}" -P 1'.format(name, exp_label))
