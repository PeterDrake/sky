"""
	Creates a csv file in RESULTS_DIR/EXPERIMENT_LABEL/ called 'mask_agreement.csv'.

	The file 'mask_agreement.csv' contains timestamp_utc and agreement data for each available timestamp from the
	files:
	shcu_typical_data.csv
	tiny_data.csv

	Note: this script gets the timestamps from these files, but it is possible that not all of these timestamps have
	simplified tsi sky images and masks available in the TYPICAL_DATA_DIR and DUBIOUS_DATA_DIR directories. This is
	especially true if the user has decided to run a smaller version of the experiment by setting SMALL_PROCESS_SIZE to
	a value other than None in config.py. This script simply skips the agreement calculation for timestamps which are
	missing the tsi or network decision image.

	Agreement is defined as the percentage of the network decision image that exactly matches the tsi decision image.
"""

import matplotlib.image as mpimg
from config import *
from utils import *


def compute_agreement(df, data_directory, csv_name):
	"""Computes the agreement between network-processed decision images and tsi decision images then creates a csv file
	with the given name in the results directory."""
	with open(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/' + csv_name, 'w') as file:
		file.write('timestamp_utc,agreement\n')

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

			# Calculate the agreement rate
			cm = np.corrcoef(tsi_mask.flat, net_mask.flat)
			agreement_rate = cm[0, 1]

			# Write agreement rate into csv file
			file.write(str(time) + ',' + str(agreement_rate) + '\n')


# Load data for the tsi (only the timestamp_utc column)
typical_tsi_df = pd.read_csv(TYPICAL_DATA_CSV)
typical_tsi_df = typical_tsi_df.filter(['timestamp_utc'])
dubious_tsi_df = pd.read_csv(DUBIOUS_DATA_CSV)
dubious_tsi_df = dubious_tsi_df.filter(['timestamp_utc'])

# Load data for the network mask (only timestamps_utc column)
typical_network_df = pd.read_csv(RESULTS_DIR + "/" + EXPERIMENT_LABEL + "/typical_fsc.csv")
typical_network_df = typical_network_df.filter(['timestamp_utc'])
dubious_network_df = pd.read_csv(RESULTS_DIR + "/" + EXPERIMENT_LABEL + "/dubious_fsc.csv")
dubious_network_df = dubious_network_df.filter(['timestamp_utc'])

# Join typical and drop missing timestamps
typical_data_df = typical_network_df.join(typical_tsi_df.set_index('timestamp_utc'), on='timestamp_utc')
typical_data_df = typical_data_df.dropna()  # Drop rows with missing values from mismatched timestamps

# Join dubious and drop missing timestamps
dubious_data_df = dubious_network_df.join(dubious_tsi_df.set_index('timestamp_utc'), on='timestamp_utc')
dubious_data_df = dubious_data_df.dropna()  # Drop rows with missing values from mismatched timestamps

# Compute the agreement rates for typical and dubious data and save the results in csv files
compute_agreement(typical_data_df, TYPICAL_DATA_DIR, 'typical_agreement.csv')
compute_agreement(dubious_data_df, DUBIOUS_DATA_DIR, 'dubious_agreement.csv')
