"""
	Creates a bunch of preliminary plots to be used for identifying examples to be used a paper or poster.

	Finds timestamps for which the network output has good agreement with the arscl data. Good agreement can be defined
	by some threshold of % within the value.

	Finds timestamps for which the network output has poor agreement with the arscl data. Poor agreement can be defined
	by some threshold of % away from the value.

	May also choose to do some for high cloud fraction, low cloud fractions, etc. Mainly comparing ARSCL and Network
	cf / fsc.

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
# tiny_fake_dubious_data.csv
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

# ============================================= Query # 1: "Good" ==================================================== #
# Define parameters used for thresholding data from our data frames. LOWER_CF and HIGHER_CF define the lower and upper
# bounds of values of cloud fraction we wish to observe. FSC_SIMILARITY is the maximum difference in fractional sky
# cover between the TSI and the network we wish to observe.
LOWER_CF = 0.3
HIGHER_CF = 0.6
FSC_SIMILARITY = 0.01

# Now we reassign typical_data_df and dubious_data_df so that they match our query.
q1_typical = typical_data_df[(LOWER_CF <= typical_data_df['cf_tot']) & (typical_data_df['cf_tot'] <= HIGHER_CF) & (
		(typical_data_df['net_fsc_z'] - typical_data_df['fsc_z']) ** 2 <= FSC_SIMILARITY ** 2)]
q1_dubious = dubious_data_df[(LOWER_CF <= dubious_data_df['cf_tot']) & (dubious_data_df['cf_tot'] <= HIGHER_CF) & (
		(dubious_data_df['net_fsc_z'] - dubious_data_df['fsc_z']) ** 2 <= FSC_SIMILARITY ** 2)]
q1 = pd.concat([q1_typical, q1_dubious]).sort_index(axis=1)

# Print the number of timestamps found in this query
print("Query #1: Typical len = " + str(len(q1_typical.index)) + ", Dubious len = " + str(len(q1_dubious.index)))


# ============================================== Query # 2: "Bad" ==================================================== #
# Define parameters used for thresholding data from our data frames. LOWER_CF and HIGHER_CF define the lower and upper
# bounds of values of cloud fraction we wish to observe. FSC_SIMILARITY is the minimum difference in fractional sky
# cover between the TSI and the network we wish to observe.
LOWER_CF = 0.3
HIGHER_CF = 0.6
FSC_SIMILARITY = 0.2  # Inverted meaning -- this is the minimum difference

# Now we reassign typical_data_df and dubious_data_df so that they match our query.
q2_typical = typical_data_df[(LOWER_CF <= typical_data_df['cf_tot']) & (typical_data_df['cf_tot'] <= HIGHER_CF) & (
		(typical_data_df['net_fsc_z'] - typical_data_df['fsc_z']) ** 2 >= FSC_SIMILARITY ** 2)]
q2_dubious = dubious_data_df[(LOWER_CF <= dubious_data_df['cf_tot']) & (dubious_data_df['cf_tot'] <= HIGHER_CF) & (
		(dubious_data_df['net_fsc_z'] - dubious_data_df['fsc_z']) ** 2 >= FSC_SIMILARITY ** 2)]
q2 = pd.concat([q2_typical, q2_dubious]).sort_index(axis=1)

# Print the number of timestamps found in this query
print("Query #2: Typical len = " + str(len(q2_typical.index)) + ", Dubious len = " + str(len(q2_dubious.index)))

# ============================================= Query # 3: "Good" ==================================================== #
# Define parameters used for thresholding data from our data frames. LOWER_CF and HIGHER_CF define the lower and upper
# bounds of values of cloud fraction we wish to observe. AGREEMENT is the minimum agreement between the TSI and the
# network decision images we wish to observe.
LOWER_CF = 0.3
HIGHER_CF = 0.6
AGREEMENT = 0.85

# Need to gather the agreement data for typical and dubious data
typical_agree_df = pd.read_csv(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/typical_agreement.csv')
typical_agree_df = typical_agree_df.join(typical_data_df.set_index('timestamp_utc'), on='timestamp_utc')
typical_agree_df = typical_agree_df.dropna()
dubious_agree_df = pd.read_csv(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/dubious_agreement.csv')
dubious_agree_df = dubious_agree_df.join(dubious_data_df.set_index('timestamp_utc'), on='timestamp_utc')
dubious_agree_df = dubious_agree_df.dropna()

# Now we reassign typical_agree_df and dubious_agree_df so that they match our query.
q3_typical = typical_agree_df[(LOWER_CF <= typical_agree_df['cf_tot']) & (typical_agree_df['cf_tot'] <= HIGHER_CF) & (
			typical_agree_df['agreement'] >= AGREEMENT)]
q3_dubious = dubious_agree_df[(LOWER_CF <= dubious_agree_df['cf_tot']) & (dubious_agree_df['cf_tot'] <= HIGHER_CF) & (
			dubious_agree_df['agreement'] >= AGREEMENT)]
q3 = pd.concat([q3_typical, q3_dubious]).sort_index(axis=1)

# Print the number of timestamps found in this query
print("Query #3: Typical len = " + str(len(q3_typical.index)) + ", Dubious len = " + str(len(q3_dubious.index)))

# ============================================== Query # 4: "Bad" ==================================================== #
# Define parameters used for thresholding data from our data frames. LOWER_CF and HIGHER_CF define the lower and upper
# bounds of values of cloud fraction we wish to observe. AGREEMENT is the maximum agreement between the TSI and the
# network decision images we wish to observe.
LOWER_CF = 0.3
HIGHER_CF = 0.6
AGREEMENT = 0.70  # Inverted meaning -- this is the maximum agreement

# Now we reassign typical_agree_df and dubious_agree_df so that they match our query.
q4_typical = typical_agree_df[(LOWER_CF <= typical_agree_df['cf_tot']) & (typical_agree_df['cf_tot'] <= HIGHER_CF) & (
			typical_agree_df['agreement'] <= AGREEMENT)]
q4_dubious = dubious_agree_df[(LOWER_CF <= dubious_agree_df['cf_tot']) & (dubious_agree_df['cf_tot'] <= HIGHER_CF) & (
			dubious_agree_df['agreement'] <= AGREEMENT)]
q4 = pd.concat([q4_typical, q4_dubious]).sort_index(axis=1)

# Print the number of timestamps found in this query
print("Query #4: Typical len = " + str(len(q4_typical.index)) + ", Dubious len = " + str(len(q4_dubious.index)))


# ============================================== Query # 5: "Bad" ==================================================== #
# Define parameters used for thresholding data from our data frames. LOWER_CF and HIGHER_CF define the lower and upper
# bounds of values of cloud fraction we wish to observe. AGREEMENT is the maximum agreement between the TSI and the
# network decision images we wish to observe.
TSI_U = 0.3  # Less than
TSI_L = 0.1  # Greater than

NET_U = 0.3  # Less than
NET_L = 0.1  # Greater than

CF = 0.01  # Less than

# Now we reassign typical_agree_df and dubious_agree_df so that they match our query.
q5_typical = typical_data_df[(typical_data_df['cf_tot'] <= CF) & (typical_data_df['fsc_z'] <= TSI_U) & (typical_data_df['fsc_z'] >= TSI_L) & (typical_data_df['net_fsc_z'] >= NET_L) & (typical_data_df['net_fsc_z'] <= NET_U)]
q5_dubious = dubious_data_df[(dubious_data_df['cf_tot'] <= CF) & (dubious_data_df['fsc_z'] <= TSI_U) & (dubious_data_df['fsc_z'] >= TSI_L) & (dubious_data_df['net_fsc_z'] >= NET_L) & (dubious_data_df['net_fsc_z'] <= NET_U)]

q5 = pd.concat([q5_typical, q5_dubious]).sort_index(axis=1)

# Print the number of timestamps found in this query
print("Query #5: Typical len = " + str(len(q5_typical.index)) + ", Dubious len = " + str(len(q5_dubious.index)))


# =========================================== Make plots for Queries ================================================= #

# Make plots for Query #1: "Good"
make_plots(q1_typical, TYPICAL_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q1', 1, len(q1.index))
make_plots(q1_dubious, DUBIOUS_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q1', len(q1_typical.index) + 1, len(q1.index))

# Make plots for Query #2: "Bad"
make_plots(q2_typical, TYPICAL_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q2', 1, len(q2.index))
make_plots(q2_dubious, DUBIOUS_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q2', len(q2_typical.index) + 1, len(q2.index))

# Make plots for Query #3: "Good"
make_plots(q3_typical, TYPICAL_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q3', 1, len(q3.index))
make_plots(q3_dubious, DUBIOUS_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q3', len(q3_typical.index) + 1, len(q3.index))

# Make plots for Query #4: "Bad"
make_plots(q4_typical, TYPICAL_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q4', 1, len(q4.index))
make_plots(q4_dubious, DUBIOUS_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q4', len(q4_typical.index) + 1, len(q4.index))

# Make plots for Query #5: "Sunglare"
make_plots(q5_typical, TYPICAL_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q5', 1, len(q5.index))
make_plots(q5_dubious, DUBIOUS_DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/finding_figs_q5', len(q5_typical.index) + 1, len(q5.index))
