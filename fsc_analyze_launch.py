"""
Plots a comparison between network and the TSI measurements of fractional sky cover. Also compares both sources to
the Laser Ceilometer.

This script can be run after fsc_launch.py has been run and its tasks have finished.

This script requires four files: 'shcu_good_data.csv', 'shcu_bad_data.csv', 'good_fsc.csv', and 'bad_fsc.csv'.
* The 'shcu' files should be located in the good_data/ and bad_data/ directories.
* The 'fsc' files should be located in the results/EXP_LABEL/ directory. EX: results/e70-00/good_fsc.csv
Both of these requirements should be satisfied if the previous scripts have been run correctly.

This script creates two plots and saves them as 'good_tsi_arscl_fsc.png' and 'compare_tsi_network_fsc.png' in the
results/EXP_LABEL/ directory.
"""

import pickle
import heapq

import numpy as np
from fsc_launch import INPUT_DATA_CSV
from poster_stamps_launch import BAD_VALID_FILE
from utils import read_csv_file, extract_data_from_dataframe, extract_data_for_date_from_dataframe
from preprocess_stamps_launch import VALID_STAMP_PATH  # TODO: Make this a bit more clear..
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

N_SAMPLES = 2500
EXP_LABEL = 'e81-00'


def load_pickled_file(filename):
	"""Loads a pickled file."""
	with open(filename, 'rb') as f:
		return pickle.load(f)


def find_worst_results(filename, num_worst=5):
	"""Finds the timestamps with the largest disagreement between network and TSI decision images. Returns a
	dictionary of length num_worst where the key is the disagreement rate and the value is the timestamp."""
	frame = read_csv_file(filename)
	net_times = set(extract_data_from_dataframe(frame, "timestamp_utc"))
	shcu = read_csv_file(INPUT_DATA_CSV)
	shcu_times = set(extract_data_from_dataframe(shcu, "timestamp_utc"))
	times = net_times.intersection(shcu_times)
	disagreement_rates = [(-1, '')] * num_worst
	heapq.heapify(disagreement_rates)
	for t in times:
		t = int(t)
		net_fsc = extract_data_for_date_from_dataframe("fsc_z", t, frame)
		shcu_fsc = extract_data_for_date_from_dataframe("fsc_z", t, shcu)
		diff = (abs(net_fsc - shcu_fsc), t)
		heapq.heappushpop(disagreement_rates, diff)
	return sorted(disagreement_rates)


def extract_arscl_and_image_fsc_from_dataframes(arscl_dataframe, image_dataframe, arscl_header="cf_tot",
                                                image_header="fsc_z"):
	"""Returns lists containing fractional sky cover obtained from two dataframes. Expects 'image_dataframe' to be a
	pandas dataframe with a header for 'fsc_z' and expects 'arscl_dataframe' to be a pandas dataframe with a header
	for 'cf_tot'. Expects both dataframes to have a header for 'timestamp_utc'. Additionally expects the dataframes to
	be clean in the aforementioned categories. I.e. NaN values are not permitted. Please us df.dropna() or some other
	method to handle missing values."""
	image_times = set(extract_data_from_dataframe(image_dataframe, "timestamp_utc"))
	arscl_times = set(extract_data_from_dataframe(arscl_dataframe, "timestamp_utc"))
	times = image_times.intersection(arscl_times)  # Necessary to correct for missing times
	x, y, residual, residual1 = [], [], [], []
	mse = 0
	for t in times:
		x.append(extract_data_for_date_from_dataframe(arscl_header, t, arscl_dataframe))
		y.append(extract_data_for_date_from_dataframe(image_header, t, image_dataframe))
		mse += (y[-1] - x[-1]) ** 2
		residual.append(abs(y[-1] - x[-1]))
		residual1.append(y[-1] - x[-1])
	return x, y, (mse / len(times)) ** 0.5, np.array(residual), np.array(residual1)


def residual_to_quartiles(residual):
	"""Sorts a list of residual errors and returns the 25th and 75th quartiles."""
	residual = sorted(list(residual))
	q25 = residual[int(0.25 * len(residual))]
	q50 = residual[int(0.50 * len(residual))]
	q75 = residual[int(0.75 * len(residual))]
	return q25, q50, q75


def scatter_plot(scatter, name, ylabel, title, xlabel):
	"""Makes a plot with the given parameters"""
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.scatter(scatter[0], scatter[1], s=0.5)
	plt.plot([0, 1], [0, 1], c='orange', lw=2)
	plt.savefig('results/' + EXP_LABEL + name, dpi=300)
	plt.close()


if __name__ == "__main__":

	# Reads data from shcu_good_data.csv, takes a sample of the times, and gets data for plotting
	good_arscl_dataframe = read_csv_file('good_data/shcu_good_data.csv')  # Contains both ARSCL and TSI Data
	good_arscl_dataframe = good_arscl_dataframe.dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	good_times = load_pickled_file(VALID_STAMP_PATH)
	good_times = good_times[0:N_SAMPLES]
	good_arscl_dataframe = good_arscl_dataframe[good_arscl_dataframe['timestamp_utc'].isin(good_times)]
	good_arscl_tsi = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_arscl_dataframe)

	# Reads data from shcu_bad_data.csv, takes a sample of the times, and gets data for plotting
	bad_arscl_dataframe = read_csv_file('bad_data/shcu_bad_data.csv')  # Contains both ARSCL and TSI Data
	bad_arscl_dataframe = bad_arscl_dataframe.dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	bad_times = load_pickled_file(BAD_VALID_FILE)  # Change this to TEST_FILE for final plotting.
	bad_times = bad_times[0:N_SAMPLES]
	bad_arscl_dataframe = bad_arscl_dataframe[bad_arscl_dataframe['timestamp_utc'].isin(bad_times)]
	bad_arscl_tsi = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_arscl_dataframe)

	# Reads data from good_fsc.csv and uses the times sample from shcu_good_data.csv to get data for plotting
	good_network_dataframe = read_csv_file('results/' + EXP_LABEL + '/good_fsc.csv')  # Contains NETWORK Data
	good_network_dataframe = good_network_dataframe.dropna(subset=['fsc_z', 'timestamp_utc'])
	good_network_dataframe = good_network_dataframe[good_network_dataframe['timestamp_utc'].isin(good_times)]
	good_arscl_network = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_network_dataframe)

	# Reads data from bad_fsc.csv and uses the times sample from shcu_bad_data.csv to get data for plotting
	bad_network_dataframe = read_csv_file('results/' + EXP_LABEL + '/bad_fsc.csv')  # Contains NETWORK Data
	bad_network_dataframe = bad_network_dataframe.dropna(subset=['fsc_z', 'timestamp_utc'])
	bad_network_dataframe = bad_network_dataframe[bad_network_dataframe['timestamp_utc'].isin(bad_times)]
	bad_arscl_network = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_network_dataframe)

	# Gets comparison data for TSI and Network decision images on good and bad data
	good_tsi_network = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_network_dataframe,
	                                                               arscl_header="fsc_z")
	bad_tsi_network = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_network_dataframe,
	                                                              arscl_header="fsc_z")

	# Good/Bad Data FSC vs CF Plots for TSI and Network Decision Images
	titles = ['Good Data', 'Bad Data']
	ylabels = ['FSC (TSI)', 'FSC (Network)']
	xlabels = ['Ceilometer CF'] * 2
	data = [good_arscl_tsi, bad_arscl_tsi, good_arscl_network, bad_arscl_network]
	fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 9), sharey=True, sharex=True)
	for ax, col in zip(axes[0], titles):
		ax.set_title(col, fontsize=30)
	for ax, row in zip(axes[:, 0], ylabels):
		ax.set_ylabel(row, fontsize=26)
	for ax, col in zip(axes[-1], xlabels):
		ax.set_xlabel(col, fontsize=26)
	for i, ax in enumerate(axes.ravel()):
		ax.tick_params(labelsize='x-large')
		ax.scatter(data[i][0], data[i][1], s=50, alpha=0.3)
		ax.plot([0, 1], [0, 1], lw=4, color='orange')
	fig.tight_layout()
	fig.savefig("results/" + EXP_LABEL + "/fsc_analyze_image_arscl.png")
	# plt.show()

	# RMSE plot
	# data to plot
	n_groups = 2
	tsi_rsme = (good_arscl_tsi[2], bad_arscl_tsi[2])
	network_rsme = (good_arscl_network[2], bad_arscl_network[2])
	fig = plt.figure(figsize=(12, 9))
	index = np.arange(n_groups)
	bar_width = 0.3
	ax = fig.add_subplot(111)
	ax.tick_params(labelsize='x-large')
	ax.bar(index, tsi_rsme, bar_width, label='TSI')
	ax.bar(index + bar_width, network_rsme, bar_width, color='orange', label='Network')
	# plt.yticks(fontsize=20)
	plt.ylabel('Root Mean Squared Error', fontsize=26)
	plt.title('Fractional Sky Cover RMSE', fontsize=30)
	ax.tick_params(
		axis='x',  # changes apply to the x-axis
		which='both',  # both major and minor ticks are affected
		bottom=False,  # ticks along the bottom edge are off
		top=False,  # ticks along the top edge are off
		labelbottom=True)
	plt.xticks((index + bar_width / 2), ('Good Data', 'Bad Data'), fontsize=26)
	ax.legend(fontsize=20)
	fig.savefig("results/" + EXP_LABEL + "/fsc_rmse_barchart.png")
