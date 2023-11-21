import unittest
import shutil
from pandas.testing import assert_frame_equal
from subprocess import check_output
from Preprocessor import *


class TestPreprocessor(unittest.TestCase):

    def setUp(self):
        print('WARNING: Some of these tests only verify that the results of the preprocessing exist.')
        print('For a more thorough test, delete your test_data directory before running them.')
        self.preprocessor = Preprocessor('../test_raw_data', '../test_raw_csv', '../test_data', verbose=True)

    def test_finds_raw_photo_path(self):
        # The os.path.normcase calls should make this work on both Windows and *nix systems
        self.assertEqual(os.path.normcase('../test_raw_data/SkyImage/sgptsiskyimageC1.a1.20180418.000000/sgptsiskyimageC1.a1.20180418.000330.jpg.20180418000330.jpg'),
                         os.path.normcase(self.preprocessor.raw_photo_path('20180418000330')))

    def test_notices_missing_raw_photo_path(self):
        self.assertIsNone(self.preprocessor.raw_photo_path('19000418000330'))

    def test_finds_raw_photo(self):
        self.assertTrue(self.preprocessor.photo_exists('20180418000330'))

    def test_notices_missing_raw_photo(self):
        self.assertFalse(self.preprocessor.photo_exists('20180418000215'))

    def test_notices_zero_byte_photo(self):
        # We added this zero-byte file to the test data
        self.assertFalse(self.preprocessor.photo_exists('20180418000245'))

    def test_finds_raw_tsi_mask_path(self):
        self.assertEqual('../test_raw_data/CloudMask/sgptsicldmaskC1.a1.20180418/sgptsicldmaskC1.a1.20180418.000330.png.20180418000330.png',
                         self.preprocessor.raw_tsi_mask_path('20180418000330'))

    def test_notices_missing_raw_tsi_mask_path(self):
        self.assertIsNone(self.preprocessor.raw_tsi_mask_path('19000418000330'))

    def test_finds_raw_tsi_mask(self):
        self.assertTrue(self.preprocessor.tsi_mask_exists('20180418000330'))

    def test_notices_missing_raw_tsi_mask(self):
        self.assertFalse(self.preprocessor.tsi_mask_exists('20180418000215'))

    def test_notices_zero_byte_tsi_mask(self):
        # We added this zero-byte file to the test data
        self.assertFalse(self.preprocessor.tsi_mask_exists('20180418000245'))

    def test_finds_correct_numbers_of_valid_and_invalid_timestamps(self):
        self.preprocessor.validate_csv('tiny_data.csv')
        self.assertEqual(309, self.preprocessor.valid_timestamp_count)
        self.assertEqual(2, self.preprocessor.invalid_timestamp_count)

    def test_writes_clean_csv(self):
        self.preprocessor.write_clean_csv('tiny_data.csv')
        data = pd.read_csv('../test_data/tiny_data.csv')
        # For this file, the clean version has 304 valid timestamps
        self.assertEqual(309, len(data))

    def test_creates_image_directories(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('tiny_data.csv')
        dirs = [self.preprocessor.data_dir + '/' + date for date in
                ['photos/20180418', 'photos/20180419', 'tsi_masks/20180418', 'tsi_masks/20180419']]
        # Run the method
        self.preprocessor.create_image_directories('tiny_data.csv')
        # Assert that the directories are present
        for d in dirs:
            self.assertTrue(os.path.isdir(d))

    def test_preprocesses_files(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('tiny_data.csv')
        # Only do the expensive preprocessing if it hasn't already been done
        if not os.path.exists(timestamp_to_photo_path(self.preprocessor.data_dir, '20180418000200')):
            print('Doing expensive preprocessing of test files')
            self.preprocessor.preprocess_images('tiny_data.csv')
        # Now check if some of the files exist
        files = [timestamp_to_photo_path(self.preprocessor.data_dir, '20180418000200'),
                 timestamp_to_photo_path(self.preprocessor.data_dir, '20180419000200'),
                 timestamp_to_tsi_mask_path(self.preprocessor.data_dir, '20180418000200'),
                 timestamp_to_tsi_mask_path(self.preprocessor.data_dir, '20180419000200')]
        for f in files:
            self.assertTrue(os.path.exists(f))


if __name__ == '__main__':
    unittest.main()
