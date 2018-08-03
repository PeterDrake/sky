"""
This script is intended to be run after preprocess_stamps_launch.py has completed its task.

Expects the TRAIN_INPUT_DIR directory to contain the following items:
	test.stamps
	train.stamps
	valid.stamps
	always_black_mask.png
	simpleimage/
	simplemask/

Launches the training process.
"""

import os

# Specify the experiment number. EX: 'e73'
exp_number = 'e76'

# Specify the number of networks to train. (Might depend on how much of BLT is in use. Recommended at least 2 if
# possible)
num_networks = 1

# Specify the location of the cropped sky photos and simplified decision images, e.g. "good_data"
TRAIN_INPUT_DIR = "good_data"

# Specify the batch size, the learning rate, and the number of training steps to complete
BATCH_SIZE = 50
LEARNING_RATE = 0.0001
TRAINING_STEPS = 2000

# Specify the number of cores for BLT. BLT currently does not actually allocate this number of cores for your job,
# but instead uses this number as a way to limit the number of jobs on a node. Training uses tensorflow,
# which automatically takes advantage of all available resources, so by default the job will use the entire node. To
# stop training batches from competing with each other for compute resources, set this to a number larger than half
# of the cores on a single node. For the summer of 2018, 25 works well.
num_cores = 25

# Specify the structure of the network. This defines how train.py constructs the network to train.
variants = [
	'a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f '
	'h:concat-g-in i:conv-3-5-h']

if __name__ == "__main__":
	i = 0
	for v in variants:
		for j in range(num_networks):
			exp_label = exp_number + '-{:0>2}'.format(i)
			condition = exp_label + ' ' + v
			os.system('SGE_Batch -r "{}" -c "python3 -u train.py {}" -P {}'.format(exp_label, condition, num_cores))
			i += 1
