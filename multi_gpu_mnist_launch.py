import os
from config import *

if __name__ == "__main__":
	for i in range(6):
		os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 multi_gpu_mnist.py" -P {}'.format('multi-gpu-results-' + str(i), JOB_PRIORITY))