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

if __name__ == '__main__':
	unittest.main()
