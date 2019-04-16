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
import csv
import scipy
import matplotlib.image as mpimg

#start a loop that goes through all the timestamps in the typical and dubious df
def find_agreement_rate(df, data_directory):

	for _, row in df.iterrows():
		time = str(int(row['timestamp_utc']))

		#try to load the decision image from the timestamp
		tsi_mask = extract_mask_path_from_time(time, data_directory)
		net_mask = extract_network_mask_path_from_time(time, EXPERIMENT_LABEL)

		#Load images from their path and do a continue if there is some error
		try:
			tsi_mask = mpimg.imread(tsi_mask)
			net_mask = mpimg.imread(net_mask)
		except FileNotFoundError:
			continue

		#calculate the agreement rate
		# already an array np.asarray(tsi_mask)
		cm = np.corrcoef(tsi_mask.flat, net_mask.flat)
		agreement_rate = cm[0,1] #TODO clarify: is this agreement rate or disagreement rate

		#write agreement rate into csv file
		filewriter.writerow([time, agreement_rate])

# Step 1 is to load the timestamp data from the shcu files.

#load data for the tsi (only the timestamp_utc column)
typical_tsi_df = pd.read_csv(TYPICAL_DATA_CSV)
typical_tsi_df = typical_tsi_df.filter(['timestamp_utc'])
dubious_tsi_df = pd.read_csv(DUBIOUS_DATA_CSV)
dubious_tsi_df = dubious_tsi_df.filter(['timestamp_utc'])

#load data for the network mask (only timestamps_utc column)
typical_network_df = pd.read_csv(RESULTS_DIR + "/" + EXPERIMENT_LABEL + "/typical_fsc.csv")
typical_network_df = typical_network_df.filter(['timestamp_utc'])
dubious_network_df = pd.read_csv(RESULTS_DIR + "/" + EXPERIMENT_LABEL + "/dubious_fsc.csv")
dubious_network_df = dubious_network_df.filter(['timestamp_utc'])

#join typical and drop missing timestamps
typical_data_df = typical_network_df.join(typical_tsi_df.set_index('timestamp_utc'), on='timestamp_utc')
typical_data_df = typical_data_df.dropna()  # Drop rows with missing values from mismatched timestamps

#join dubious and drop missing timestamps
dubious_data_df = dubious_network_df.join(dubious_tsi_df.set_index('timestamp_utc'), on='timestamp_utc')
dubious_data_df = dubious_data_df.dropna()  # Drop rows with missing values from mismatched timestamps

# Step 2 is to define and create the csv file to store the results.

#TODO determine where the csv file is going to be saved. RESULTS_DIR + '/' + EXPERIMENT_LABEL + 'mask_agreement.csv'
with open(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/mask_agreement.csv', 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',')
	filewriter.writerow(['timestamp_utc', 'agreement_rate'])

# Step 3 is the loop which goes through all the timestamp data. Each iteration of the loop should do a try/except to
# load the tsi and network decision images from the timestamp, doing a continue if there is some error. Each iteration
# of the loop should compute the number of pixels that are the same in both images, then record the percentage in the
# csv file
	find_agreement_rate(typical_data_df, TYPICAL_DATA_DIR)

	find_agreement_rate(dubious_data_df, DUBIOUS_DATA_DIR)

# Step 4 is to close the file and do anything else that I haven't thought of yet
csvfile.close()

# Step 5 is to update make_agreement_plots.py so that it uses a variety of thresholds to help us find "good", "bad" and
# "medium" data types. I think having between 30-60% fsc or cf should be used in most of these because it makes the
# image more interesting.