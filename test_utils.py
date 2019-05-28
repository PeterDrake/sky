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
		timestamps = {'20170920195000', '20170920195030', '20170920195100', '20170920195130', '20170920195200'}
		self.assertEqual(timestamps, extract_all_times('/Users/student/PycharmProjects/sky/test_data/test_simplemask'))

	def test_extracts_times_from_filenames(self):
		filenames = {'simplemask20170920195000.png', 'simplemask20170920195030.png', 'simplemask20170920195100.png',
					 'simplemask20170920195130.png', 'simplemask20170920195200.png'}
		times = {'20170920195000', '20170920195030', '20170920195100', '20170920195130', '20170920195200'}
		self.assertEqual(times, extract_times_from_filenames(filenames))

	def test_extracts_times_from_file(self):
		timestamps = {'20170920195000\n', '20170920195030\n', '20170920195100\n', '20170920195130\n', '20170920195200'}
		self.assertEqual(timestamps, extract_times_from_file('test_data/test_filename'))

	def test_clean_csv(self):
		with open("test_data/test_csv.csv", "w+") as f:
			f.write("There are spaces and one , in this sentence.")
		clean_csv('test_data/test_csv.csv')
		with open("test_data/test_csv.csv", "r") as f:
			self.assertEqual("Therearespacesandone,inthissentence.", f.read())
		os.remove('test_data/test_csv.csv')

	def test_is_series(self):
		series = pd.Series()
		not_series = {1, 2, 3}
		self.assertEqual(True, is_series(series))
		self.assertEqual(False, is_series(not_series))

	def test_all_duplicates_in_data(self):
		data = pd.Series([1, 1, 1, 1, 1])
		data2 = pd.Series([1, 2, 3, 4, 5])
		self.assertEqual(False, all_duplicates(data2))
		self.assertEqual(True, all_duplicates(data))

	def test_extract_first_element_in_data(self):
		series = pd.Series([1, 2, 3, 4, 5])
		self.assertEqual(1, pick_duplicate(series))

	def test_create_img_path(self):
		dir = 'sky/test_data'
		self.assertEqual('sky/test_data/simpleimage/2017/0814/', img_save_path('20170814092430', dir))

	def test_create_mask_path(self):
		dir = 'sky/test_data'
		self.assertEqual('sky/test_data/simplemask/2017/0814/', mask_save_path('20170814092430', dir))

	def test_extract_img_path_from_time(self):
		dir = 'sky/test_data'
		self.assertEqual('sky/test_data/simpleimage/2017/0814/simpleimage20170814092430.jpg',
		extract_img_path_from_time('20170814092430', dir))

	def test_extract_mask_path_from_time(self):
		dir = 'sky/test_data'
		self.assertEqual('sky/test_data/simplemask/2017/0814/simplemask20170814092430.png',
		extract_mask_path_from_time('20170814092430', dir))

	def test_extract_mask_path_from_time_raw(self):
		self.assertEqual('sky/CloudMask/sgptsicldmaskC1.a1.20170814/sgptsicldmaskC1.a1.20170814.092430.png.20170814092430.png',
		extract_mask_path_from_time_raw('20170814092430', 'sky'))




if __name__ == '__main__':
	unittest.main()
