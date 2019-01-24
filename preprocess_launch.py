"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) First follow steps outlined in preprocess_setup_launch.py
2) Run this program to launch all of the batches necessary on BLT.

This program launches preprocess.py for each file in the 'res' folder in the OUTPUT_DIR.
"""

import os


batches = os.listdir('typical_data' + '/res')
for i, batch in enumerate(batches):
	# TODO Make this more flexible.
	os.system('SGE_Batch -r "{}" -c "python3 -u preprocess.py {}" -P 1'.format('pre-batch-{}'.format(i), 'typical_data' + '/res/' + batch))

batches = os.listdir('dubious_data' + '/res')
for i, batch in enumerate(batches):
	# TODO Make this more flexible.
	os.system('SGE_Batch -r "{}" -c "python3 -u preprocess.py {}" -P 1'.format('pre-batch-{}'.format(i), 'dubious_data' + '/res/' + batch))
