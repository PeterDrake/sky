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

	def test_year_month_day_are_extracted(self):
		self.assertEqual('20150208', time_to_year_month_day(20150208093000))

	def test_hour_minute_second_are_extracted(self):
		self.assertEqual('093000', time_to_hour_minute_second(20150208093000))

	def test_timestamp_is_extracted_from_filename(self):
		self.assertEqual('20150208093000',
				extract_timestamp('sgptsicldmaskC1.a1.20150208.093000.png.20150208093000.png'))
		self.assertEqual('20150208093000',
				extract_timestamp('sgptsiskyimageC1.a1.20150208.093000.jpg.20150208093000.jpg'))

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
