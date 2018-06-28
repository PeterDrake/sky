from utils import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
	# TODO: read in the network's csv file for timestamps and fsc_z
	# TODO: read in shcu_good_data to get the arscl estimate for fsc.
	# TODO: plot net fsc on y, arscl on the x axis

	net_label = "e70-00"
	net_fsc_path = "results/" + net_label + "/fsc.csv"

	net_frame = read_csv_file(net_fsc_path)
	net_times = net_frame.get("timestamp_utc")

	arscl_frame = read_csv_file("shcu_good_data.csv")

	with plt.xkcd():
		net_fsc, arscl_fsc = [], []
		for t in net_times:
			net_fsc.append(extract_data_for_date_from_dataframe(net_frame, t, "fsc_z"))
			arscl_fsc.append(extract_data_for_date_from_dataframe(arscl_frame, t, "cf_tot"))
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		ax.set_xlabel("ARSCL fsc")
		ax.set_ylabel("Network fsc")
		ax.set_title("Fractional Sky Cover Comparison")
		ax.plot(arscl_fsc, net_fsc)
		plt.tight_layout()
		fig.savefig('results/' + net_label + '/fractional_sky_cover_comparison.png', dpi=300, bbox_inches='tight')
