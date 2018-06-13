import os


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


def listdir_d(dir=None):
	"""Returns an iterable of directories in the current or a given directory."""
	return (name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name)))


def listdir_f(dir=None):
	"""Returns an iterable of files in the current of a given directory."""
	return (name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name)))
