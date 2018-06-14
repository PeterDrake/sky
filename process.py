"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) First follow steps outlined in preprocess.py
2) Run this program to launch all of the batches necessary on BLT.

This program launches process_batch.py with each file in the 'res' folder.
"""

import os

batches = os.listdir('res')
for batch in batches:
	os.system('SGE_Batch -r "{}" -c "python3 -u process_batch.py {}" -P 1'.format(batch[:-4], "res/" + batch))
	print("Launched {} successfully".format(batch))
