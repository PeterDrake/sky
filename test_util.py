import unittest

from utils import *


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

	def test_year_month_day_are_extracted(self):
		self.assertEqual('20150208', time_to_year_month_day(20150208093000))

	def test_hour_minute_second_are_extracted(self):
		self.assertEqual('093000', time_to_hour_minute_second(20150208093000))

	def test_timestamp_is_extracted_from_filename(self):
		self.assertEqual('20150208093000',
				extract_timestamp('sgptsicldmaskC1.a1.20150208.093000.png.20150208093000.png'))
		self.assertEqual('20150208093000',
				extract_timestamp('sgptsiskyimageC1.a1.20150208.093000.jpg.20150208093000.jpg'))

	def test_exp_label_is_extracted_from_filename(self):
		self.assertEqual('e70-00', extract_exp_label('networkmask_e70-00.20160411234030.png'))
		self.assertEqual('e70-01', extract_exp_label('networkmask_e70-01.20150208093000.png'))

	def test_all_timestamps_are_extracted(self):
		self.assertEqual(20, len(extract_all_times(self.INPUT_DIR, ['/SkyImage', '/CloudMask'])))

	def test_times_are_extracted_from_files(self):
		mask_path = self.INPUT_DIR + "/CloudMask/sgptsicldmaskC1.a1.20131118/"
		image_path = self.INPUT_DIR + "SkyImage/sgptsiskyimageC1.a1.20131118.131600/"
		masks = ['sgptsicldmaskC1.a1.20131118.133230.png.20131118133230.png',
			'sgptsicldmaskC1.a1.20131118.133300.png.20131118133300.png']
		images = ['sgptsiskyimageC1.a1.20131118.133200.jpg.20131118133200.jpg',
			'sgptsiskyimageC1.a1.20131118.133230.jpg.20131118133230.jpg']
		files = [mask_path + m for m in masks] + [image_path + i for i in images]
		actual = {'20131118133200', '20131118133230', '20131118133300'}
		self.assertEqual(actual, extract_times_from_filenames(files))

	def test_extract_tsi_fsc_from_csv(self):
		self.assertEqual(0.300045, extract_tsi_fsc_for_date(20120501170900))
		self.assertEqual(0.256652, extract_tsi_fsc_for_date(20120501170230))
		self.assertEqual(0.530595, extract_tsi_fsc_for_date(20120501170500))

	def test_extract_ceilometer_fsc_from_csv(self):
		csv = read_csv_file("shcu_good_data.csv")

		def shorten(t):
			return math.floor(extract_data_for_date_from_dataframe("cf_tot", t, csv) * 10 ** 6) / 10 ** 6

		self.assertEqual(0.368888, shorten(20120501170900))
		self.assertEqual(0.44, shorten(20120501170230))
		self.assertEqual(0.431111, shorten(20120501170500))

	def test_extract_fsc_for_date_from_dataframe(self):
		csv = read_csv_file("shcu_good_data.csv")

		def shorten(t):
			return math.floor(extract_data_for_date_from_dataframe("fsc_z", t, csv) * 10 ** 6) / 10 ** 6

		self.assertEqual(0.300045, shorten(20120501170900))
		self.assertEqual(0.00, shorten(20120513004100))
		self.assertEqual(0.002511, shorten(20150911230730))
