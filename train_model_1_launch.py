"""
Launches the training process.
"""

import os
from config import *

if __name__ == "__main__":
	os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u train_model_1.py" -P {}'.format('keras_train_4', JOB_PRIORITY))