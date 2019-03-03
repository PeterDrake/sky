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

# Specify the structure of the network. This defines how train.py constructs the network to train.
net = 'a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-4-h'

if __name__ == "__main__":
	if BLT:
		os.system('SGE_Batch -r "{}" -c "python3 -u train.py {}" -P {}'.format(EXPERIMENT_LABEL, net, JOB_PRIORITY))
	else:
		train(net)

