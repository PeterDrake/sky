"""
Launches the training process.
"""

import os
from config import *

if __name__ == "__main__":
	run_name = 'keras_train_8'
	os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u train_model_1.py {}" -P {}'.format(run_name, True, JOB_PRIORITY))