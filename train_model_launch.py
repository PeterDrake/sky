"""
Launches the training process.
"""

import os
from config import *

if __name__ == "__main__":
	run_name = MODEL_TYPE
	os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u train_model.py {}" -P {}'.format(run_name, True, JOB_PRIORITY))