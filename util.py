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
	return str(time)[0:8]


def time_to_hour_minute_second(time):
	return str(time)[8:14]

def extract_timestamp(filename):
	"""Returns the timestamp within filename. Assumes filename ends in something like 20160415235930.jpg or
	20160415235930.png."""
	return filename[-18:-4]


def extract_times_from_directory(dir):
	"""Returns an iterable of timestamps within a directory. Assumes filenames ends in something like
	20160415235930.jpg or
	20160415235930.png."""
	return (extract_timestamp(name) for name in listdir_d(dir))


def extract_times_from_files(files):
	"""Returns an iterable of timestamps extracted from an iterable collection of files."""
	return (extract_timestamp(file) for file in files)


def extract_timestamp_recur(dir):
	"""Returns timestamps from all sub-directories"""
	dirpath, subdirs, files = os.walk(dir)
	return extract_times_from_files(files)


def listdir_d(dir=None):
	"""Returns an iterable of directories in the current or a given directory."""
	return (name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name)))


def listdir_f(dir=None):
	"""Returns an iterable of files in the current of a given directory."""
	return (name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name)))