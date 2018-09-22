"""
Plots a comparison between network and the TSI measurements of fractional sky cover. Also compares both sources to
the Laser Ceilometer.

This file is typically run from fsc_analyze_launch.py, but can be run from the command line with an argument for the
experiment label.
EX: python3 fsc_analyze.py e70-00

This script requires four files: 'shcu_good_data.csv', 'shcu_bad_data.csv', 'good_fsc.csv', and 'bad_fsc.csv'.
* The 'shcu' files should be located in the same directory as this file.
* The 'fsc' files should be located in the results/exp_label/ directory. EX: results/e70-00/good_fsc.csv

This script creates two plots and saves them as 'good_tsi_arscl_fsc.png' and 'compare_tsi_network_fsc.png' in the
results/exp_label/ directory.
"""

import pickle
import heapq
import sys

import numpy as np
from fsc_launch import INPUT_DATA_CSV
from poster_stamps_launch import BAD_VALID_FILE
from utils import read_csv_file, extract_data_from_dataframe, extract_data_for_date_from_dataframe
from preprocess_stamps_launch import VALID_STAMP_PATH  # TODO: Make this a bit more clear..
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


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


def scatter_plot(title, xlabel, ylabel, scatter, name):
	"""Makes a plot with the given parameters"""
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.scatter(scatter[0], scatter[1], s=0.5)
	plt.plot([0, 1], [0, 1], c='orange', lw=2)
	plt.savefig('results/' + exp_label + name, dpi=300)
	plt.close()


if __name__ == "__main__":
	N_SAMPLES = 2500
	# exp_label = sys.argv[1].decode('utf-8')
	exp_label = 'e76-00'

	# Reads data from shcu_good_data.csv, takes a sample of the times, and gets data for plotting
	good_arscl_dataframe = read_csv_file('shcu_good_data.csv')  # Contains both ARSCL and TSI Data
	good_arscl_dataframe = good_arscl_dataframe.dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	good_times = load_pickled_file(VALID_STAMP_PATH)
	good_times = good_times[0:N_SAMPLES]
	good_arscl_dataframe = good_arscl_dataframe[good_arscl_dataframe['timestamp_utc'].isin(good_times)]
	good_arscl_tsi = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_arscl_dataframe)

	# Reads data from shcu_bad_data.csv, takes a sample of the times, and gets data for plotting
	bad_arscl_dataframe = read_csv_file('shcu_bad_data.csv')  # Contains both ARSCL and TSI Data
	bad_arscl_dataframe = bad_arscl_dataframe.dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	bad_times = load_pickled_file(BAD_VALID_FILE)  # Change this to TEST_FILE for final plotting.
	bad_times = bad_times[0:N_SAMPLES]
	bad_arscl_dataframe = bad_arscl_dataframe[bad_arscl_dataframe['timestamp_utc'].isin(bad_times)]
	bad_arscl_tsi = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_arscl_dataframe)

	# Reads data from good_fsc.csv and uses the times sample from shcu_good_data.csv to get data for plotting
	good_network_dataframe = read_csv_file('results/' + exp_label + '/good_fsc.csv')  # Contains NETWORK Data
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

	# TODO: Uncomment below to plot with rmse
	# good_tsi_rmse, good_network_rmse = good_arscl_tsi[2], good_arscl_network[2]
	# bad_tsi_rmse, bad_network_rmse = bad_arscl_tsi[2], bad_arscl_network[2]
	#
	# good_tsi_quartiles = residual_to_quartiles(good_arscl_tsi[3])
	# good_network_quartiles = residual_to_quartiles(good_arscl_network[3])
	# bad_tsi_quartiles = residual_to_quartiles(bad_arscl_tsi[3])
	# bad_network_quartiles = residual_to_quartiles(bad_arscl_network[3])
	#
	# x_data = [' TSI ', ' NETWORK ', 'TSI', 'NETWORK']
	# rmse_data = [good_tsi_rmse, good_network_rmse, bad_tsi_rmse, bad_network_rmse]
	# lower_error = [good_tsi_quartiles[0], good_network_quartiles[0], bad_tsi_quartiles[0], bad_network_quartiles[0]]
	# upper_error = [good_tsi_quartiles[2], good_network_quartiles[2], bad_tsi_quartiles[2], bad_network_quartiles[2]]
	# for i in range(4):
	# 	lower_error[i] = rmse_data[i] - lower_error[i]
	# 	upper_error[i] -= rmse_data[i]
	#
	# plt.title("")
	# plt.ylabel("FSC Difference")
	# plt.xlabel("GOOD DATA                                                                BAD DATA")
	# plt.tick_params(
	# 		axis='x',  # changes apply to the x-axis
	# 		which='both',  # both major and minor ticks are affected
	# 		bottom=True,  # ticks along the bottom edge are on
	# 		top=True,  # ticks along the top edge are on
	# 		labelbottom=True)  # labels along the bottom edge are on
	# plt.errorbar(x_data, rmse_data, yerr=[lower_error, upper_error], fmt='.', ecolor='orange', capsize=4)
	# plt.plot(x_data, rmse_data, 'o', label="RMSE")
	# plt.tight_layout()
	# plt.legend()
	# plt.show()
	# TODO: End uncomment here

	# TODO: Uncomment to plot with median instead
	# good_tsi_rmse, good_network_rmse = good_arscl_tsi[2], good_arscl_network[2]
	# bad_tsi_rmse, bad_network_rmse = bad_arscl_tsi[2], bad_arscl_network[2]
	#
	# good_tsi_quartiles = residual_to_quartiles(good_arscl_tsi[4])
	# good_network_quartiles = residual_to_quartiles(good_arscl_network[4])
	# bad_tsi_quartiles = residual_to_quartiles(bad_arscl_tsi[4])
	# bad_network_quartiles = residual_to_quartiles(bad_arscl_network[4])
	#
	# x_data = [' TSI ', ' NETWORK ', 'TSI', 'NETWORK']
	# median_data = [good_tsi_quartiles[1], good_network_quartiles[1], bad_tsi_quartiles[1], bad_network_quartiles[1]]
	# lower_error = [good_tsi_quartiles[0], good_network_quartiles[0], bad_tsi_quartiles[0], bad_network_quartiles[0]]
	# upper_error = [good_tsi_quartiles[2], good_network_quartiles[2], bad_tsi_quartiles[2], bad_network_quartiles[2]]
	# for i in range(4):
	# 	lower_error[i] = median_data[i] - lower_error[i]
	# 	upper_error[i] -= median_data[i]
	#
	# plt.title("")
	# plt.ylabel("FSC Difference")
	# plt.xlabel("GOOD DATA                                                                BAD DATA")
	# plt.tick_params(
	# 		axis='x',  # changes apply to the x-axis
	# 		which='both',  # both major and minor ticks are affected
	# 		bottom=True,  # ticks along the bottom edge are on
	# 		top=True,  # ticks along the top edge are on
	# 		labelbottom=True)  # labels along the bottom edge are on
	# plt.errorbar(x_data, median_data, yerr=[lower_error, upper_error], fmt='.', ecolor='orange', capsize=4)
	# plt.plot(x_data, median_data, 'o', label="Median")
	# plt.tight_layout()
	# plt.legend()
	# plt.show()
	# TODO: End uncomment

	# Makes plots of FSC vs CF for TSI and Network on good and bad data
	# scatter_plot('Good Data', 'Ceilometer CF', 'Total Sky Imager FSC', good_arscl_tsi, '/good_tsi_ceilometer.png')
	# scatter_plot('Bad Data', 'Ceilometer CF', 'Total Sky Imager FSC', bad_arscl_tsi, '/bad_tsi_ceilometer.png')
	# scatter_plot('Good Data', 'Ceilometer CF', 'Network FSC', good_arscl_network, '/good_network_ceilometer.png')
	# scatter_plot('Bad Data', 'Ceilometer CF', 'Network FSC', bad_arscl_network, '/bad_network_ceilometer.png')

	# # Makes four plots for the performance comparison and prints out the Root Mean Squared Error
	# x_label = 'CF SHCU'
	# # y_labels = ['TSI FSC'] * 2 + ['NETWORK FSC'] * 2
	# y_labels = ['NETWORK FSC'] * 2
	# titles = ['Good Data', 'Bad Data']
	# DATA = [good_arscl_network, bad_arscl_network]
	# fig = plt.figure(figsize=(12, 4))
	# for i, data in enumerate(DATA):
	# 	ax = fig.add_subplot(1, 2, i + 1)
	# 	ax.set_aspect('auto')
	# 	ax.set_ylabel(y_labels[i])
	# 	ax.set_xlabel(x_label)
	# 	ax.set_title(titles[i] + " ({})".format(i + 1))
	# 	plt.plot([0, 1], [0, 1], c='orange', lw=2)
	# 	plt.scatter(data[0], data[1], s=.5)
	# # plt.tight_layout()
	# plt.savefig("results/" + exp_label + "/fsc_analyze_image_arscl.png", dpi=300)
	# for i, data in enumerate(DATA):
	# 	print("The RMSE for plot {} is {}.".format(i + 1, data[2]))
	#
	# # Makes two plots for direct comparison between TSI and Network on good and bad data
	# fig2 = plt.figure(figsize=(12, 8))
	# titles = ["Good Data", "Bad Data"]
	# DATA = [good_tsi_network, bad_tsi_network]
	# for i, title in enumerate(titles):
	# 	ax = fig2.add_subplot(1, 2, i + 1)
	# 	ax.set_xlabel("TSI FSC")
	# 	ax.set_ylabel("NETWORK FSC")
	# 	ax.set_title(title)
	# 	plt.scatter(DATA[i][0], DATA[i][1], s=0.5)
	# 	plt.plot([0, 1], [0, 1], c='orange', lw=2)
	# plt.tight_layout()
	# plt.savefig("results/" + exp_label + "/fsc_analyze_tsi_network.png", dpi=300)
	# print("The RMSE for TSI/NET on GOOD DATA is {}.".format(good_tsi_network[2]))
	# print("The RMSE for TSI/NET on BAD DATA is {}.".format(bad_tsi_network[2]))

	# Makes four plots for the performance comparison and prints out the Root Mean Squared Error
	# x_label = 'CF SHCU'
	# y_labels = ['TSI FSC'] * 2 + ['NETWORK FSC'] * 2
	# titles = ['Good Data', 'Bad Data', 'Good Data', 'Bad Data']
	# DATA = [good_arscl_tsi, bad_arscl_tsi, good_arscl_network, bad_arscl_network]
	# fig = plt.figure(figsize=(12, 9))
	# for i, data in enumerate(DATA):
	# 	ax = fig.add_subplot(2, 2, i + 1)
	# 	ax.set_ylabel(y_labels[i], fontsize=18)
	# 	ax.set_xlabel(x_label, fontsize=18)
	# 	ax.set_title(titles[i], fontsize=26)
	# 	plt.yticks(fontsize=14)
	# 	plt.xticks(fontsize=14)
	# 	plt.plot([0, 1], [0, 1], c='orange', lw=4)
	# 	plt.scatter(data[0], data[1], s=40, alpha=0.3)
	# plt.tight_layout()
	# plt.savefig("results/" + exp_label + "/fsc_analyze_image_arscl.png", dpi=300)
	# for i, data in enumerate(DATA):
	# 	print("The RMSE for plot {} is {}.".format(i + 1, data[2]))
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
	fig.savefig("results/" + exp_label + "/fsc_analyze_image_arscl.png")
	# plt.show()


	# RMSE plot
	# data to plot
	n_groups = 2
	tsi_rsme = (good_arscl_tsi[2], bad_arscl_tsi[2])
	network_rsme = (good_arscl_network[2], bad_arscl_network[2])

	# create plot
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
	fig.savefig("results/" + exp_label + "/fsc_rmse_barchart.png")
