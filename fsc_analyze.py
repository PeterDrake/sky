"""Compares the fsc values in fsc.csv file of each network to the shcu_good_data.csv"""

import heapq

import matplotlib.pyplot as plt

from analyze import disagreement_rate
from utils import *


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
		net_fsc = extract_fsc_for_date_from_dataframe(frame, t)
		shcu_fsc = extract_fsc_for_date_from_dataframe(shcu, t)
		diff = (abs(net_fsc - shcu_fsc), t)
		heapq.heappushpop(disagreement_rates, diff)
	return sorted(disagreement_rates)


def show_network_arscl_tsi_fsc(image_dataframe, arscl_dataframce):
	x = list()
	y = list()
	i = 0
	image_times = set(extract_data_from_dataframe(image_dataframe, "timestamp_utc"))
	print("first converted to set")
	arscl_times = set(extract_data_from_dataframe(arscl_dataframce, "timestamp_utc"))
	print("second converted to set")
	times = image_times.intersection(arscl_times)
	print("found intersection")
	for t in times:
		image_fsc = extract_data_for_date_from_dataframe("fsc_z", t, image_dataframe)
		arscl_fsc = extract_data_for_date_from_dataframe("cf_tot", t, arscl_dataframce)
		x.append(arscl_fsc)
		y.append(image_fsc)
		i += 1
		if i % 1000 == 0:
			print(i)
	return x, y

# TODO: This doesn't show the fsc difference at all. Currently configured to show pixel difference, if it even works.
def show_plot_of_fsc_difference(timestamps, exp_label, directory):
	rates = np.zeros(len(timestamps))
	for i, t in enumerate(timestamps):
		if os.path.isfile(extract_network_mask_path_from_time(t, exp_label)) and os.path.isfile(
				extract_mask_path_from_time(t, 'good_data')):
			tsi_mask = get_simple_mask(t)
			our_mask = get_network_mask_from_time_and_label(t, exp_label)
			rates[i] = disagreement_rate(our_mask, tsi_mask)
		else:
			print("not here")
			pass
	# Save a graph of accuracies
	with plt.xkcd():
		fig, ax = plt.subplots(nrows=1, ncols=1)
		ax.plot(np.take(rates * 100, np.flip((rates.argsort()), axis=0)))
		ax.set_ylabel('Percent of Pixels Incorrect')
		ax.set_xlabel('Masks (sorted by accuracy)')
		ax.set_title("Pixel disagreement rate between our masks and TSI masks")
		fig.savefig(directory + '/' + exp_label + '/' + exp_label + 'accuracy_plot.png', bbox_inches='tight')


if __name__ == "__main__":
	image_csv = read_csv_file('shcu_good_data.csv').dropna(subset=['fsc_z', 'cf_tot', 'timestamp_utc'])
	print("done reading in csv")
	x, y = show_network_arscl_tsi_fsc(image_csv, image_csv)
	plt.plot(x, y, "Fsc Agreement Rate")
# net_csv_path = sys.argv[1]
# print("The biggest differences in fsc occur during the times: \n<{}>".format(find_worst_results(net_csv_path)))
