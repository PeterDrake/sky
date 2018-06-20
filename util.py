import math
import os

import pandas as pd


def time_to_year(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the year as a string."""
	return str(time)[0:4]


def time_to_month(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the month as a string."""
	return str(time)[4:6]


def time_to_day(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the day as a string."""
	return str(time)[6:8]


def time_to_month_and_day(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the 'mmdd'."""
	return str(time)[4:8]


def time_to_year_month_day(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the 'yyyymmdd'."""
	return str(time)[0:8]


def time_to_hour_minute_second(time):
	"""Time must be in the format yyyymmddhhmmss. Returns the 'hhmmss'."""
	return str(time)[8:14]


def extract_timestamp(filename):
	"""Returns the timestamp within filename. Assumes filename ends in something like 20160415235930.jpg or
	20160415235930.png."""
	return filename[-18:-4]


def extract_exp_label(filename):
	"""Returns the experiment label within filename of networkmasks. Assumes filename ends in something like e70-00.20160415235930.png"""
	return filename[-25:-19]

def extract_all_times(dir, subdirs=None):
	"""Returns timestamps from all directories that are within the input directory. You can specify a list of
	subdirectories if you only want to grab files within specific subdirectories.
	Ex: dir/masks/mask20160411000000.jpg would be extracted, and
		dir/masks/folder/mask20160411000000.jpg would also be extracted."""
	times = set()
	if not subdirs:
		for dirpath, subdirs, files in os.walk(dir):
			for file in files:
				times.add(extract_timestamp(file))
	else:
		for subdir in subdirs:
			for dirpath, subdirs, files in os.walk(dir + subdir):
				for file in files:
					times.add(extract_timestamp(file))
	return times


def extract_times_from_filenames(filenames):
	"""Returns an iterable of timestamps extracted from an iterable collection of files."""
	return {extract_timestamp(filename) for filename in filenames}


def extract_times_from_file(filename):
	"""Returns a set of timestamps in a given file. Assumes timestamps are separated by newlines."""
	times = set()
	with open(filename, 'r') as file:
		for time in file:
			times.add(str(time))
	return times


def extract_data_from_csv(filename, column_header):
	"""Returns a list of data from a csv file. Assumes the csv has headers."""
	data = pd.read_csv(filename).get(column_header)
	return {str(d) for d in data}


def extract_tsi_fsc_for_bad_dates(timestamps):
	nan_fsc = set()
	csv = read_csv_file("shcu_good_data.csv")
	df = csv.set_index("timestamp_utc", drop=False)
	# drop=False to not delete timestamp_utc column if other index set later
	for time in timestamps:
		fsc_value = df.loc[time, "fsc_z"]
		if fsc_value == 0:
			nan_fsc.add(time)
	return nan_fsc


def extract_tsi_fsc_for_date(timestamp):
	csv = read_csv_file("shcu_good_data.csv")
	df = csv.set_index("timestamp_utc", drop=False)
	# drop=False to not delete timestamp_utc column if other index set later
	return (math.floor(df.loc[timestamp, "fsc_z"] * 10 ** 6)) / 10 ** 6


def extract_ceilometer_fsc_for_date(timestamp):
	csv = read_csv_file("shcu_good_data.csv")
	df = csv.set_index("timestamp_utc", drop=False)
	# drop=False to not delete timestamp_utc column if other index set later
	return (math.floor(df.loc[timestamp, "cf_tot"] * 10 ** 6)) / 10 ** 6


def read_csv_file(filename):
	"""Reads a csv file using the pandas csv reader and returns a pandas data frame."""
	return pd.read_csv(filename)


def listdir_d(dir=None):
	"""Returns an iterable of directories in the current or a given directory."""
	return (name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name)))


def listdir_f(dir=None):
	"""Returns an iterable of files in the current of a given directory."""
	return (name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name)))
