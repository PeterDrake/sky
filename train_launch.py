"""
This script is intended to be run after preprocess_stamps_launch.py has completed its task.

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

# Specify the experiment number. EX: 'e73'
exp_number = 'e82'

# Specify the structure of the network. This defines how train.py constructs the network to train.
variants = [
	'a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f '
	'h:concat-g-in i:conv-3-4-h']

if __name__ == "__main__":
	i = 0
	for v in variants:
		for j in range(NUM_NETWORKS):
			exp_label = exp_number + '-{:0>2}'.format(i)
			condition = exp_label + ' ' + v
			if BLT:
				os.system('SGE_Batch -r "{}" -c "python3 -u train.py {}" -P {}'.format(exp_label, condition, JOB_PRIORITY))
			else:
				train(exp_label, v)
			i += 1
