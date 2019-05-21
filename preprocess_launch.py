import os
import time
from config import *
from preprocess import preprocess


if __name__ == "__main__":
	start = time.clock()
	# Runs preprocessing for typical data
	batches = os.listdir(TYPICAL_DATA_DIR + '/res')
	for i, batch in enumerate(batches):
		if BLT:
			os.system('SGE_Batch -r "{}" -c "python3 -u preprocess.py {} {}" -P 1'.format('typical-pre-batch-{}'.format(i), TYPICAL_DATA_DIR + '/res/' + batch, TYPICAL_DATA_DIR))
		else:
			preprocess(TYPICAL_DATA_DIR + '/res/' + batch, TYPICAL_DATA_DIR)

	# Runs preprocessing for dubious data
	batches = os.listdir(DUBIOUS_DATA_DIR + '/res')
	for i, batch in enumerate(batches):
		if BLT:
			os.system('SGE_Batch -r "{}" -c "python3 -u preprocess.py {} {}" -P 1'.format('dubious-pre-batch-{}'.format(i), DUBIOUS_DATA_DIR + '/res/' + batch, DUBIOUS_DATA_DIR))
		else:
			preprocess(DUBIOUS_DATA_DIR + '/res/' + batch, DUBIOUS_DATA_DIR)
	print("Time elapsed: " + str(time.clock() - start) + " seconds.")
