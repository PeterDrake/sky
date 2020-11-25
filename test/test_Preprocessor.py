import unittest

from Preprocessor import *


class TestCleanCsv(unittest.TestCase):

    def setUp(self):
        self.preprocessor = Preprocessor('../test_data')

    def test_finds_raw_photo_path(self):
        self.assertEqual('../test_data/SkyImage/sgptsiskyimageC1.a1.20180418.000000/sgptsiskyimageC1.a1.20180418.000330.jpg.20180418000330.jpg',
                         self.preprocessor.raw_photo_path('20180418000330'))

    def test_notices_missing_raw_photo_path(self):
        self.assertIsNone(self.preprocessor.raw_photo_path('19000418000330'))

    def test_finds_raw_photo(self):
        self.assertTrue(self.preprocessor.photo_exists('20180418000330'))

    def test_notices_missing_raw_photo(self):
        self.assertFalse(self.preprocessor.photo_exists('20180418000215'))

    def test_notices_zero_byte_photo(self):
        # We added this zero-byte file to the test data
        self.assertFalse(self.preprocessor.photo_exists('20180418000245'))

    # def test_finds_raw_tsi_mask_path(self):
    #     self.assertEqual('../test_data/SkyImage/sgptsiskyimageC1.a1.20180418.000000/sgptsiskyimageC1.a1.20180418.000330.jpg.20180418000330.jpg',
    #                      self.preprocessor.raw_photo_path('20180418000330'))
    #
    # def test_notices_missing_raw_tsi_mask_path(self):
    #     self.assertIsNone(self.preprocessor.raw_photo_path('19000418000330'))

if __name__ == '__main__':
    unittest.main()
