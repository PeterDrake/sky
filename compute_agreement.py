"""
	Creates a csv file in RESULTS_DIR/EXPERIMENT_LABEL/ called 'mask_agreement.csv'.

	The file 'mask_agreement.csv' contains timestamp_utc and agreement data for each available timestamp from the files:
	shcu_typical_data.csv
	shcu_dubious_data.csv

	Note: this script gets the timestamps from these files, but it is possible that not all of these timestamps have
	simplified tsi sky images and masks available in the TYPICAL_DATA_DIR and DUBIOUS_DATA_DIR directories. This is
	especially true if the user has decided to run a smaller version of the experiment by setting SMALL_PROCESS_SIZE to
	a value other than None in config.py. This script simply skips the agreement calculation for timestamps which are
	missing the tsi or network decision image.

	Agreement is defined as the percentage of the network decision image that exactly matches the tsi decision image.
"""

from config import *
from utils import *

# Step 1 is to load the timestamp data from the shcu files.


# Step 2 is to define and create the csv file to store the results.


# Step 3 is the loop which goes through all the timestamp data. Each iteration of the loop should do a try/except to
# load the tsi and network decision images from the timestamp, doing a continue if there is some error. Each iteration
# of the loop should compute the number of pixels that are the same in both images, then record the percentage in the
# csv file


# Step 4 is to close the file and do anything else that I haven't thought of yet


# Step 5 is to update make_agreement_plots.py so that it uses a variety of thresholds to help us find "good", "bad" and
# "medium" data types. I think having between 30-60% fsc or cf should be used in most of these because it makes the
# image more interesting.