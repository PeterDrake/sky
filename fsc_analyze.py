"""Compares the fsc values in fsc.csv file of each network to the shcu_good_data.csv"""

import heapq
import sys

from utils import *


def find_worst_results(filename, num_worst=5):
	frame = read_csv_file(filename)
	shcu = read_csv_file('shcu_good_data.csv')
	disagreement_rates = [(-1, '')] * num_worst
	heapq.heapify(disagreement_rates)
	times = extract_data_from_dataframe(frame, "timestamp_utc")
	for t in times:
		net_fsc = extract_fsc_for_date_from_dataframe(frame, t)
		shcu_fsc = extract_fsc_for_date_from_dataframe(shcu, t)
		diff = (abs(net_fsc - shcu_fsc), t)
		heapq.heappushpop(disagreement_rates, diff)
	return sorted(disagreement_rates)


if __name__ == "__main__":
	net_csv_path = sys.argv[1]
	print(find_worst_results(net_csv_path))
