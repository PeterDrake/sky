
# def time_to_year(time):
# 	"""Time must be an integer in the format yyyymmddhhmmss. Returns the year as an integer."""
# 	return time // 1e10
#
# def time_to_month(time):
# 	"""Time must be an integer in the format yyyymmddhhmmss. Returns the month as an integer."""
# 	return time // 1e8 - (time // 1e10) * 1e2
#
# def time_to_month_and_day(time):
# 	"""Time must be an integer in the format yyyymmddhhmmss. Returns the month & day as an integer."""
# 	return time // 1e6 - (time // 1e10) * 1e4

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

def get_times_from_directory(dir):
	pass