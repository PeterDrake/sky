import os
from util import time_to_year, time_to_month_and_day


def create_dirs(output_dir, times):
	"""Creates directories for simpleimage and simplemask in the output_dir as well as creating subdirectories by year
	and day for the given timestamps. Expects the input_dir and output_dir to be relative to the current working
	directory. Pass in an iterable collection of timestamps in the yyyymmddhhmmss format."""
	# if not times:
	# 	times = os.listdir(input_dir) #If time not specified, use everything in the input directory.
	seen = {} #yyyy, set(mmdd, ...)
	for t in times:
		year = time_to_year(t)
		mmdd = time_to_month_and_day(t)
		if year not in seen.keys():
			seen[year] = set()
		seen[year].add(mmdd)
	for year in seen.keys():
		os.makedirs(output_dir + "/simpleimage/" + year)
		os.makedirs(output_dir + "/simplemask/" + year)
		for mmdd in seen[year]:
			os.makedirs(output_dir + "/simpleimage/" + year + "/" + mmdd)
			os.makedirs(output_dir + "/simplemask/" + year + "/" + mmdd)
	return
