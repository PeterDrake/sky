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
import pandas as pd

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

print(typical_data_df.head())
# print(dubious_data_df.head())

# Define parameters used for thresholding data from our data frames. LOWER_CF and HIGHER_CF define the lower and upper
# bounds of values of cloud fraction we wish to observe. FSC_SIMILARITY is the maximum difference in fractional sky
# cover between the TSI and the network we wish to observe.
LOWER_CF = 0.3
HIGHER_CF = 0.6
FSC_SIMILARITY = 0.2

# Now we reassign typical_data_df and dubious_data_df so that they match our query.
typical_data_df = typical_data_df[(LOWER_CF <= typical_data_df['cf_tot']) & (typical_data_df['cf_tot'] <= HIGHER_CF) & (
			(typical_data_df['net_fsc_z'] - typical_data_df['fsc_z']) ** 2 <= FSC_SIMILARITY ** 2)]
dubious_data_df = dubious_data_df[(LOWER_CF <= dubious_data_df['cf_tot']) & (dubious_data_df['cf_tot'] <= HIGHER_CF) & (
			(dubious_data_df['net_fsc_z'] - dubious_data_df['fsc_z']) ** 2 <= FSC_SIMILARITY ** 2)]


print(typical_data_df.head())
