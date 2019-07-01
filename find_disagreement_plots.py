"""
	Creates a bunch of preliminary plots to be used for identifying examples to be used a paper or poster.

	Finds timestamps for which the network output and the tsi have disagreement with each other in cloud fraction and agreement.
	Agreement is the diffrence in pixles when comparing the tsi and the network. Agreement is calculated in compute_agreement.py

	Saves triptych plots of the sky image, tsi mask, and network mask to a location in the results directory for a
	specific network. This plot includes the timestamp, good/bad data, the fsc/cf under each image. Also a barchart for
	those values on the right side of the plot.
"""

from config import *
from utils import *
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def make_plots(df, data_directory, save_path, i, num_rows):
	# Now we need to iterate over our data frame and load images into memory for plotting.
	os.makedirs(save_path, exist_ok=True)
	df = df.head(num_rows)
	for _, row in df.iterrows():  # Note: itertuples would be slightly faster, but iterrows is easier to use.
		# Make the timestamp usable (Without this timestamps would end in '.0').
		time = str(int(row['timestamp_utc']))

		# Extract image and mask paths from the timestamp
		sky_image = extract_img_path_from_time(time, data_directory)
		tsi_mask = extract_mask_path_from_time(time, data_directory)
		net_mask = extract_network_mask_path_from_time(time, EXPERIMENT_LABEL)

		# Load the actual images from their paths
		try:
			sky_image = mpimg.imread(sky_image)
			tsi_mask = mpimg.imread(tsi_mask)
			net_mask = mpimg.imread(net_mask)
		except FileNotFoundError:
			print("Couldn't find one of:")
			print("\t" + extract_img_path_from_time(time, data_directory))
			print("\t" + extract_mask_path_from_time(time, data_directory))
			print("\t" + extract_network_mask_path_from_time(time, EXPERIMENT_LABEL))
			continue

		# Display the images in a plot together
		fig, (ax0, ax1, ax2, ax3) = plt.subplots(1, 4, figsize=(16, 4), num=i)
		fig.suptitle("Timestamp: " + time + "\n" + str(i) + " of " + str(num_rows))
		ax0.imshow(sky_image)  # ax0 is the sky image
		ax0.set_title("Sky Image")
		ax0.set_xticks([])
		ax0.set_yticks([])
		ax1.imshow(tsi_mask)  # ax1 is the tsi decision image
		ax1.set_title("TSI Decision Image")
		ax1.set_xticks([])
		ax1.set_yticks([])
		ax2.imshow(net_mask)  # ax2 is the network decision image
		ax2.set_title("Network Decision Image")
		ax2.set_xticks([])
		ax2.set_yticks([])
		ax3.set_title('FSC and CF Data')  # ax3 is our bar chart
		ax3.bar('ARSCL\nCF', row['cf_tot'], color='blue', width=0.5)
		ax3.bar('TSI\nFSC', row['fsc_z'], width=0.5)
		ax3.bar('NET\nFSC', row['net_fsc_z'], color='skyblue', width=0.5)
		ax3.set_ylim((0, 1))

		# Save the figure. Close it to save memory. Increment the figure counter
		plt.savefig(save_path + '/' + time + '.png')
		plt.close()
		i += 1


# The network fsc values can be obtained from the csv files:
# RESULTS_DIR/EXPERIMENT_LABEL/typical_fsc.csv
# RESULTS_DIR/EXPERIMENT_LABEL/dubious_fsc.csv
# Note: This obviously requires the network to be trained and for it to have processed a number of sky images. In
# addition, fsc processing needs to be done (by running fsc_launch.py after process_launch.py finishes).
typical_network_fsc_df = pd.read_csv(RESULTS_DIR + "/" + EXPERIMENT_LABEL + "/typical_fsc.csv")
dubious_network_fsc_df = pd.read_csv(RESULTS_DIR + "/" + EXPERIMENT_LABEL + "/dubious_fsc.csv")

# The tsi fsc and arscl cloud fraction values can be obtained from the csv files:
# shcu_typical_data.csv
# shcu_dubious_data.csv
# Note: The paths to these files are already defined in config.py. Additionally, note that the header for TSI fsc in the
# zenith region is 'fsc_z' and the header for arscl cloud fraction is 'cf_tot'.
typical_arscl_fsc_cf_df = pd.read_csv(TYPICAL_DATA_CSV)
dubious_arscl_fsc_cf_df = pd.read_csv(DUBIOUS_DATA_CSV)

# Drops useless columns in typical_network_fsc_df and renames 'fsc_z' to 'net_fsc_z' to prevent overloaded column names
# in a later join. Drops useless columns in typical_arscl_fsc_cf_df, then joins typical_network_fsc_df and
# typical_arscl_fsc_cf_df on 'timestamp_utc'.
typical_network_fsc_df = typical_network_fsc_df.filter(['timestamp_utc', 'fsc_z'])
typical_network_fsc_df = typical_network_fsc_df.rename(columns={'fsc_z': 'net_fsc_z'})
typical_arscl_fsc_cf_df = typical_arscl_fsc_cf_df.filter(['timestamp_utc', 'fsc_z', 'cf_tot'])
typical_data_df = typical_network_fsc_df.join(typical_arscl_fsc_cf_df.set_index('timestamp_utc'), on='timestamp_utc')
typical_data_df = typical_data_df.dropna()  # Drop rows with missing values from mismatched timestamps

# Drops useless columns in dubious_network_fsc_df and renames 'fsc_z' to 'net_fsc_z' to prevent overloaded column names
# in a later join. Drops useless columns in dubious_arscl_fsc_cf_df, then joins dubious_network_fsc_df and
# dubious_arscl_fsc_cf_df on 'timestamp_utc'.
dubious_network_fsc_df = dubious_network_fsc_df.filter(['timestamp_utc', 'fsc_z'])
dubious_network_fsc_df = dubious_network_fsc_df.rename(columns={'fsc_z': 'net_fsc_z'})
dubious_arscl_fsc_cf_df = dubious_arscl_fsc_cf_df.filter(['timestamp_utc', 'fsc_z', 'cf_tot'])
dubious_data_df = dubious_network_fsc_df.join(dubious_arscl_fsc_cf_df.set_index('timestamp_utc'), on='timestamp_utc')
dubious_data_df = dubious_data_df.dropna()  # Drop rows with missing values from mismatched timestamps

# Need to gather the agreement data for typical and dubious data
typical_agree_df = pd.read_csv(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/typical_agreement.csv')
typical_agree_df = typical_agree_df.join(typical_data_df.set_index('timestamp_utc'), on='timestamp_utc')
typical_agree_df = typical_agree_df.dropna()
dubious_agree_df = pd.read_csv(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/dubious_agreement.csv')
dubious_agree_df = dubious_agree_df.join(dubious_data_df.set_index('timestamp_utc'), on='timestamp_utc')
dubious_agree_df = dubious_agree_df.dropna()

# The number of images you want plots for
NUMBER_DISAGREEMENT_IMGS = 10

# Creates new column in data frame with the cloud fraction difference between tsi and network
typical_agree_df['cf_diff'] = (typical_agree_df['net_fsc_z'] - typical_agree_df['fsc_z']) ** 2
dubious_agree_df['cf_diff'] = (dubious_agree_df['net_fsc_z'] - dubious_agree_df['fsc_z']) ** 2

# Sort by column label agreement
typical_agree_df = typical_agree_df.sort_values(by='agreement')
dubious_agree_df = dubious_agree_df.sort_values(by='agreement')

# Takes a selected amount of timestamps determined by NUMBER_DISAGREEMENT_IMGS and creates plots
# make_plots(typical_agree_df, TYPICAL_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/disagreement_figs/typical_agreement', 1, NUMBER_DISAGREEMENT_IMGS)
# make_plots(dubious_agree_df, DUBIOUS_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/disagreement_figs/dubious_agreement', 1, NUMBER_DISAGREEMENT_IMGS)

print(typical_agree_df)

# Sort by column label cf_diff
typical_agree_df = typical_agree_df.sort_values(by='cf_diff', ascending=False)
dubious_agree_df = dubious_agree_df.sort_values(by='cf_diff', ascending=False)

# Takes a selected amount of timestamps determined by NUMBER_DISAGREEMENT_IMGS and creates plots
# make_plots(typical_agree_df, TYPICAL_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/disagreement_figs/typical_cf_diff', 1, NUMBER_DISAGREEMENT_IMGS)
# make_plots(dubious_agree_df, DUBIOUS_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/disagreement_figs/dubious_cf_diff', 1, NUMBER_DISAGREEMENT_IMGS)

print(typical_agree_df)
