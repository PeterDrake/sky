import unittest
import shutil

from Preprocessor import *


class TestPreprocessor(unittest.TestCase):

    def setUp(self):
        self.preprocessor = Preprocessor('../test_raw_data', '../test_raw_csv', '../test_data', verbose=True)

    def test_finds_raw_photo_path(self):
        self.assertEqual('../test_raw_data/SkyImage/sgptsiskyimageC1.a1.20180418.000000/sgptsiskyimageC1.a1.20180418.000330.jpg.20180418000330.jpg',
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
        self.preprocessor.validate_csv('shcu_dubious_data.csv')
        self.assertEqual(2, self.preprocessor.valid_timestamp_count)
        self.assertEqual(2, self.preprocessor.invalid_timestamp_count)

    def test_writes_clean_csv(self):
        self.preprocessor.write_clean_csv('shcu_dubious_data.csv')
        data = pd.read_csv('../test_data/shcu_dubious_data.csv')
        # For this file, the clean version only has one valid timestamp
        self.assertEqual(2, len(data))

    def test_creates_image_directories(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('shcu_dubious_data.csv')
        dirs = [self.preprocessor.data_dir + '/' + date for date in
                ['photos/20180418', 'photos/20180419', 'tsi_masks/20180418', 'tsi_masks/20180419']]
        # Destroy the existing directories
        for d in dirs:
            if os.path.isdir(d):
                shutil.rmtree(d)
        # Run the method
        self.preprocessor.create_image_directories('shcu_dubious_data.csv')
        # Assert that the directories are present
        for d in dirs:
            self.assertTrue(os.path.isdir(d))

    def test_preprocesses_files(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('shcu_dubious_data.csv')
        self.preprocessor.preprocess_images('shcu_dubious_data.csv')
        files = [self.preprocessor.data_dir + '/photos/20180418/20180418000200_photo.jpg',
                 self.preprocessor.data_dir + '/photos/20180419/20180419000200_photo.jpg',
                 self.preprocessor.data_dir + '/tsi_masks/20180418/20180418000200_tsi_mask.png',
                 self.preprocessor.data_dir + '/tsi_masks/20180419/20180419000200_tsi_mask.png']
        for f in files:
            self.assertTrue(os.path.exists(f))

    def test_counts_images_per_date(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('shcu_dubious_data.csv')
        dates = self.preprocessor.count_images_per_date('shcu_dubious_data.csv')
        correct = {'date': ['20180418', '20180419'], 'count': [1, 1]}
        self.assertEqual(correct, dates)


if __name__ == '__main__':
    unittest.main()
