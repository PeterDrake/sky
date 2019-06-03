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
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"  # specify which GPU(s) to be used
from config import *
from train import train
from utils import get_experiment_label


if __name__ == "__main__":
	for i in range(NUM_NETWORKS):
		if BLT:
			os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u train.py {} {}" -P {}'.format(get_experiment_label(i), get_experiment_label(i), NETWORK_STRUCTURE, JOB_PRIORITY))
		else:
			train(get_experiment_label(i), NETWORK_STRUCTURE.split())

