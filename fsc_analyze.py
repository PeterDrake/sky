"""
Plots a comparison between network and the TSI measurements of fractional sky cover. Also compares both sources to
the Laser Ceilometer.

This file is typically run from fsc_analyze_launch.py, but can be run from the command line with an argument for the
experiment label.
EX: python3 fsc_analyze.py e70-00

This script requires four files: 'shcu_good_data.csv', 'shcu_bad_data.csv', 'fsc.csv', and 'bad_fsc.csv'.
* The 'shcu' files should be located in the same directory as this file.
* The 'fsc' files should be located in the results/exp_label/ directory. EX: results/e70-00/fsc.csv

This script creates two plots and saves them as 'good_tsi_arscl_fsc.png' and 'compare_tsi_network_fsc.png' in the
results/exp_label/ directory.
"""

import sys
import heapq

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from fsc_launch import INPUT_DATA_CSV

from utils import read_csv_file, extract_data_from_dataframe, extract_data_from_csv, \
	extract_data_for_date_from_dataframe


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
	x, y = [], []
	mse = 0
	for t in times:
		x.append(extract_data_for_date_from_dataframe(arscl_header, t, arscl_dataframe))
		y.append(extract_data_for_date_from_dataframe(image_header, t, image_dataframe))
		mse += (y[-1] - x[-1]) ** 2
	return x, y, (mse / len(times)) ** 0.5


if __name__ == "__main__":
	N_SAMPLES = 4500
	exp_label = sys.argv[1]

	# Reads data from shcu_good_data.csv, takes a sample of the times, and gets data for plotting
	good_arscl_dataframe = read_csv_file('shcu_good_data.csv')  # Contains both ARSCL and TSI Data
	good_arscl_dataframe = good_arscl_dataframe.dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	good_times = good_arscl_dataframe.get('timestamp_utc').sample(n=N_SAMPLES)
	good_arscl_dataframe = good_arscl_dataframe[good_arscl_dataframe['timestamp_utc'].isin(good_times)]
	good_arscl_tsi = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_arscl_dataframe)

	# Reads data from shcu_bad_data.csv, takes a sample of the times, and gets data for plotting
	bad_arscl_dataframe = read_csv_file('shcu_bad_data.csv')  # Contains both ARSCL and TSI Data
	bad_arscl_dataframe = bad_arscl_dataframe.dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	bad_times = bad_arscl_dataframe.get('timestamp_utc').sample(n=N_SAMPLES)
	bad_arscl_dataframe = bad_arscl_dataframe[bad_arscl_dataframe['timestamp_utc'].isin(bad_times)]
	bad_arscl_tsi = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_arscl_dataframe)

	# Reads data from fsc.csv and uses the times sample from shcu_good_data.csv to get data for plotting
	good_network_dataframe = read_csv_file('results/' + exp_label + '/fsc.csv')  # Contains NETWORK Data
	good_network_dataframe = good_network_dataframe.dropna(subset=['fsc_z', 'timestamp_utc'])
	good_network_dataframe = good_network_dataframe[good_network_dataframe['timestamp_utc'].isin(good_times)]
	good_arscl_network = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_network_dataframe)

	# Reads data from bad_fsc.csv and uses the times sample from shcu_bad_data.csv to get data for plotting
	bad_network_dataframe = read_csv_file('results/' + exp_label + '/bad_fsc.csv')  # Contains NETWORK Data
	bad_network_dataframe = bad_network_dataframe.dropna(subset=['fsc_z', 'timestamp_utc'])
	bad_network_dataframe = bad_network_dataframe[bad_network_dataframe['timestamp_utc'].isin(bad_times)]
	bad_arscl_network = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_network_dataframe)

	# Gets comparison data for TSI and Network decision images on good and bad data
	good_tsi_network = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_network_dataframe,
			arscl_header="fsc_z")
	bad_tsi_network = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_network_dataframe,
			arscl_header="fsc_z")

	# Makes four plots for the performance comparison and prints out the Root Mean Squared Error
	x_label = 'CF SHCU'
	y_labels = ['TSI FSC'] * 2 + ['NETWORK FSC'] * 2
	titles = ['Good Data', 'Bad Data', 'Good Data', 'Bad Data']
	DATA = [good_arscl_tsi, bad_arscl_tsi, good_arscl_network, bad_arscl_network]
	fig = plt.figure(figsize=(12, 8))
	for i, data in enumerate(DATA):
		ax = fig.add_subplot(2, 2, i + 1)
		ax.set_ylabel(y_labels[i])
		ax.set_xlabel(x_label)
		ax.set_title(titles[i] + " ({})".format(i + 1))
		plt.plot([0, 1], [0, 1], c='orange', lw=2)
		plt.scatter(data[0], data[1], s=.25)
	plt.tight_layout()
	plt.savefig("results/" + exp_label + "/good_tsi_arscl_fsc.png", dpi=300)
	for i, data in enumerate(DATA):
		print("The RMSE for plot {} is {}.".format(i + 1, data[2]))

	# Makes two plots for direct comparison between TSI and Network on good and bad data
	fig2 = plt.figure(figsize=(12, 8))
	titles = ["Good Data", "Bad Data"]
	DATA = [good_tsi_network, bad_tsi_network]
	for i, title in enumerate(titles):
		ax = fig2.add_subplot(1, 2, i + 1)
		ax.set_xlabel("TSI FSC")
		ax.set_ylabel("NETWORK FSC")
		ax.set_title(title)
		plt.scatter(DATA[i][0], DATA[i][1], s=0.25)
		plt.plot([0, 1], [0, 1], c='orange', lw=2)
	plt.tight_layout()
	plt.savefig("results/" + exp_label + "/compare_tsi_network_fsc.png", dpi=300)
	print("The RMSE for TSI/NET on GOOD DATA is {}.".format(good_tsi_network[2]))
	print("The RMSE for TSI/NET on BAD DATA is {}.".format(bad_tsi_network[2]))
