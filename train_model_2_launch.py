"""
Launches the training process.
"""

import os
from config import *

if __name__ == "__main__":
	run_name = 'inception_1'
	os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u train_model_2.py {}" -P {}'.format(run_name, False, 1))