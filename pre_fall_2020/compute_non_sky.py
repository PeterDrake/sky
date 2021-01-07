"""
	Creates a csv file in RESULTS_DIR/EXPERIMENT_LABEL/ called 'non_sky.csv'.

	The file 'non_sky.csv' contains timestamp_utc and the percentage of the decision image which is non-sky for each
	available timestamp from the files:
	shcu_typical_data.csv
	tiny_fake_dubious_data.csv

	Note: this script gets the timestamps from these files, but it is possible that not all of these timestamps have
	simplified tsi sky images and masks available in the TYPICAL_DATA_DIR and DUBIOUS_DATA_DIR directories. This is
	especially true if the user has decided to run a smaller version of the experiment by setting SMALL_PROCESS_SIZE to
	a value other than None in config.py. This script simply skips the non-sky calculation for timestamps which are
	missing the tsi or network decision image.

	The non-sky percentage is defined as the percentage of the decision image which is black
"""

import matplotlib.image as mpimg
from config import *
from utils import *


def compute_nonsky(df, data_directory, csv_name, write_mode='w'):
	"""Computes the agreement between network-processed decision images and tsi decision images then creates a csv file
	with the given name in the results directory."""
	with open(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/' + csv_name, write_mode) as file:
		file.write('timestamp_utc,nonsky,net_nonsky\n')

		for _, row in df.iterrows():
			time = str(int(row['timestamp_utc']))

			# Get the paths of the decision images from their timestamps
			tsi_mask = extract_mask_path_from_time(time, data_directory)
			net_mask = extract_network_mask_path_from_time(time, EXPERIMENT_LABEL)

			# Load images from their path and do a continue if there is some error
			try:
				tsi_mask = mpimg.imread(tsi_mask)
				net_mask = mpimg.imread(net_mask)
			except FileNotFoundError:
				continue

			# Calculate the non-sky amount
			tsi_nonsky = np.count_nonzero(tsi_mask == BLACK) / (480*480*3)
			net_nonsky = np.count_nonzero(net_mask == BLACK) / (480*480*3)

			# Write non-sky amount to the csv file
			file.write(time + ',' + str(tsi_nonsky) + ',' + str(net_nonsky) + '\n')


# TODO: Make this more efficient by only using timestamps in the shcu files AND in the fsc files
df = pd.read_csv(TYPICAL_DATA_CSV)
compute_nonsky(df, TYPICAL_DATA_DIR, 'non_sky.csv')
df = pd.read_csv(DUBIOUS_DATA_CSV)
compute_nonsky(df, DUBIOUS_DATA_DIR, 'non_sky.csv', write_mode='a')