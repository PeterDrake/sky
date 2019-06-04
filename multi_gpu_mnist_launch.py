import os
from config import *


if __name__ == "__main__":
	for i in range(NUM_NETWORKS):
		os.system('SGE_Batch -q gpu.q -r -c "python3 -u multi_gpu_mnist.py" -P {}'.format(JOB_PRIORITY))