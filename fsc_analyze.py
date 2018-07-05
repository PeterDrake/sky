"""Compares the fsc values in fsc.csv file of each network to the shcu_good_data.csv"""

import heapq

import matplotlib.pyplot as plt

from utils import read_csv_file, extract_data_from_dataframe, extract_data_from_csv, \
	extract_data_for_date_from_dataframe


def find_worst_results(filename, num_worst=5):
	frame = read_csv_file(filename)
	net_times = set(extract_data_from_dataframe(frame, "timestamp_utc"))
	# print(frame)
	# print(net_times)
	shcu = read_csv_file('shcu_good_data.csv')
	shcu_times = set(extract_data_from_csv('shcu_good_data.csv', "timestamp_utc"))

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


def extract_arscl_and_image_fsc_from_dataframes(arscl_dataframe, image_dataframe):
	"""Returns lists containing fractional sky cover obtained from two dataframes. Expects 'image_dataframe' to be a
	pandas dataframe with a header for 'fsc_z' and expects 'arscl_dataframe' to be a pandas dataframe with a header
	for 'cf_tot'. Expects both dataframes to have a header for 'timestamp_utc'. Additionally expects the dataframes to
	be clean in the aforementioned categories. I.e. NaN values are not permitted. Please us df.dropna() or some other
	method to handle missing values."""
	image_times = set(extract_data_from_dataframe(image_dataframe, "timestamp_utc"))
	arscl_times = set(extract_data_from_dataframe(arscl_dataframe, "timestamp_utc"))
	times = image_times.intersection(arscl_times)
	x, y = [], []
	for i, t in enumerate(times):
		x.append(extract_data_for_date_from_dataframe("fsc_z", t, image_dataframe))
		y.append(extract_data_for_date_from_dataframe("cf_tot", t, arscl_dataframe))
	return x, y


if __name__ == "__main__":
	N_SAMPLES = 2500

	# TODO: Find better way to take random subset of data that still has good overlap. Maybe sample timestamps?

	good_arscl_dataframe = read_csv_file('shcu_good_data.csv')  # Contains both ARSCL and TSI Data
	good_arscl_dataframe = good_arscl_dataframe.dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	# good_arscl_dataframe = good_arscl_dataframe.sample(n=N_SAMPLES)
	good_arscl_dataframe = good_arscl_dataframe[0:N_SAMPLES]
	good_arscl_tsi = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_arscl_dataframe)

	good_network_dataframe = read_csv_file('results/e70-00/fsc.csv')  # Contains NETWORK Data
	good_network_dataframe = good_network_dataframe.dropna(subset=['fsc_z', 'timestamp_utc'])
	# good_network_dataframe = good_network_dataframe.sample(n=N_SAMPLES)
	good_network_dataframe = good_network_dataframe[0:N_SAMPLES]
	good_arscl_network = extract_arscl_and_image_fsc_from_dataframes(good_arscl_dataframe, good_network_dataframe)

	# TODO: Get arscl_tsi and arscl_network data for bad times

	# TODO: Plot arscl_tsi and arscl_network data for bad times
	x_label = 'ARSCL FSC'
	y_labels = ['TSI FSC'] + ['NETWORK FSC']
	DATA = [good_arscl_tsi, good_arscl_network]
	fig = plt.figure()
	with plt.xkcd():
		for i, d in enumerate(DATA):
			ax = fig.add_subplot(2, 2, i + 1)
			ax.set_xlabel(x_label)
			ax.set_ylabel(y_labels[i])
			plt.scatter(d[0], d[1], s=.5)
	plt.tight_layout()
	plt.savefig("results/e70-00/good_tsi_arscl_fsc.png")
