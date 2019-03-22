"""
This script is intended to be run after all the preprocessing tasks are completed.

Expects the TYPICAL_DATA_DIR directory to contain the following items:
	test.stamps
	train.stamps
	valid.stamps
	always_black_mask.png
	simpleimage/
	simplemask/

Launches the training process.
"""

import os
from config import *
from train import train


if __name__ == "__main__":
	if BLT:
		os.system('SGE_Batch -r "{}" -c "python3 -u train.py {}" -P {}'.format(EXPERIMENT_LABEL, NETWORK_STRUCTURE, JOB_PRIORITY))
	else:
		train(NETWORK_STRUCTURE.split())

