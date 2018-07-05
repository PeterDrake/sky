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
	times = image_times.intersection(arscl_times)  # Necessary to correct for missing times
	x, y = [], []
	for t in times:
		x.append(extract_data_for_date_from_dataframe("fsc_z", t, image_dataframe))
		y.append(extract_data_for_date_from_dataframe("cf_tot", t, arscl_dataframe))
	return x, y


if __name__ == "__main__":
	N_SAMPLES = 4000
	exp_labels = ['e70-00']

	for exp_label in exp_labels:

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
		# bad_network_dataframe = read_csv_file('results/' + exp_label + '/bad_fsc.csv')  # Contains NETWORK Data
		# bad_network_dataframe = bad_network_dataframe.dropna(subset=['fsc_z', 'timestamp_utc'])
		# bad_network_dataframe = bad_network_dataframe[bad_network_dataframe['timestamp_utc'].isin(bad_times)]
		# bad_arscl_network = extract_arscl_and_image_fsc_from_dataframes(bad_arscl_dataframe, bad_network_dataframe)

		# TODO: Get arscl_network data for bad times
		bad_arscl_network = (1, 3)
		x_labels = ['TSI FSC']*2 + ['NETWORK FSC']*2
		y_label = 'CF SHCU'
		titles = ['Good Data', 'Bad Data', 'Good Data', 'Bad Data']
		DATA = [good_arscl_tsi, bad_arscl_tsi, good_arscl_network, bad_arscl_network]
		fig = plt.figure()
		for i, d in enumerate(DATA):
			ax = fig.add_subplot(2, 2, i + 1)
			ax.set_xlabel(x_labels[i])
			ax.set_ylabel(y_label)
			ax.set_title(titles[i])
			plt.plot([0, 1], [0, 1], c='orange', lw=2)
			plt.scatter(d[1], d[0], s=.25)
		plt.tight_layout()
		plt.savefig("results/" + exp_label + "/good_tsi_arscl_fsc.png", dpi=600)
