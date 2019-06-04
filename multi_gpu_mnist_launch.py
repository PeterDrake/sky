import os
from config import *


if __name__ == "__main__":
	for i in range(NUM_NETWORKS):
		os.system('python3 multi_gpu_mnist.py')