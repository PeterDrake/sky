"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) First follow steps outlined in preprocess_setup_launch.py
2) Run this program to launch all of the batches necessary on BLT.

This program launches preprocess.py for each file in the 'res' folder in the OUTPUT_DIR.
"""

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
			os.system('SGE_Batch -r "{}" -c "python3 -u preprocess.py {} {}" -P 1'.format('typical-pre-batch-{}'.format(i), TYPICAL_DATA_DIR + '/res/' + batch, "typical_data"))
		else:
			preprocess(TYPICAL_DATA_DIR + '/res/' + batch, "typical_data")

	# Runs preprocessing for dubious data
	batches = os.listdir('dubious_data' + '/res')
	for i, batch in enumerate(batches):
		if BLT:
			os.system('SGE_Batch -r "{}" -c "python3 -u preprocess.py {} {}" -P 1'.format('dubious-pre-batch-{}'.format(i), DUBIOUS_DATA_DIR + '/res/' + batch, "dubious_data"))
		else:
			preprocess(DUBIOUS_DATA_DIR + '/res/' + batch, "dubious_data")
	print("Time elapsed: " + str(time.clock() - start) + " seconds.")
