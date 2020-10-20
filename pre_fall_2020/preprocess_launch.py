import os
import time
from config import *
from preprocess import preprocess


def launch_preprocess(directory, description):
	"""Launches preprocessing of the files in directory, using description as part of the job name if on BLT."""
	batches = os.listdir(directory + '/res')
	for i, batch in enumerate(batches):
		if BLT:
			os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u preprocess.py {} {}" -P 1'.format(description + '-pre-batch-{}'.format(i), directory + '/res/' + batch, directory))
		else:
			preprocess(directory + '/res/' + batch, directory)


if __name__ == "__main__":
	start = time.clock()
	launch_preprocess(TYPICAL_DATA_DIR, 'typical')
	launch_preprocess(DUBIOUS_DATA_DIR, 'dubious')
	print("Time elapsed: " + str(time.clock() - start) + " seconds.")
