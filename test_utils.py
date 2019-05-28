# Unit tests for utils

import unittest
from utils import *


class TestUtil(unittest.TestCase):

	def test_extracts_year_from_time(self):
		self.assertEqual('2017', time_to_year('20170814092430'))

	def test_extracts_month_from_time(self):
		self.assertEqual('08', time_to_month('20170814092430'))

	def test_extracts_day_from_time(self):
		self.assertEqual('14', time_to_day('20170814092430'))

	def test_extracts_month_and_day_from_time(self):
		self.assertEqual('0814', time_to_month_and_day('20170814092430'))

	def test_extracts_year_month_day_from_time(self):
		self.assertEqual('20170814', time_to_year_month_day('20170814092430'))

	def test_extracts_hour_minute_second_from_time(self):
		self.assertEqual('092430', time_to_hour_minute_second('20170814092430'))

	def test_extracts_timestamp(self):
		self.assertEqual('20160415235930', extract_timestamp('20160415235930.png'))

	def test_extracts_exp_label(self):
		self.assertEqual('e70-00', extract_exp_label('e70-00.20160415235930.png'))

	def test_extracts_all_times(self):
		times = {'20170920195000', '20170920195030', '20170920195100', '20170920195130', '20170920195200'}
		self.assertEqual(times, extract_all_times('/Users/student/PycharmProjects/sky/test_data/test_simplemask'))

	def test_extracts_times_from_filenames(self):
		filenames = {'simplemask20170920195000.png', 'simplemask20170920195030.png', 'simplemask20170920195100.png',
					 'simplemask20170920195130.png', 'simplemask20170920195200.png'}
		times = {'20170920195000', '20170920195030', '20170920195100', '20170920195130', '20170920195200'}
		self.assertEqual(times, extract_times_from_filenames(filenames))

	# def test_extracts_times_from_file(self):
	# 	self.assertEqual('e70-00', extract_times_from_file('e70-00.20160415235930.png'))

	# def test_clean_csv(self):



if __name__ == '__main__':
	unittest.main()
