import unittest
from util import *

class TestUtil(unittest.TestCase):
	INPUT_DIR = 'test_input'

	def test_year_is_extracted(self):
		self.assertEqual('2015', time_to_year(20150208093000))

	def test_month_is_extracted(self):
		self.assertEqual('02', time_to_month(20150208093000))

	def test_day_is_extracted(self):
		self.assertEqual('08', time_to_day(20150208093000))

	def test_month_and_day_are_extracted(self):
		self.assertEqual('0208', time_to_month_and_day(20150208093000))

	def test_extract_all_timestamps_from_directory(self):
		self.assertEqual(20, len([i for i in extract_times_from_directory(self.INPUT_DIR)]))
