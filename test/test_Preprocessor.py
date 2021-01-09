import unittest
import shutil
from pandas.testing import assert_frame_equal
from subprocess import check_output
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
        self.preprocessor.validate_csv('tiny_fake_dubious_data.csv')
        self.assertEqual(2, self.preprocessor.valid_timestamp_count)
        self.assertEqual(2, self.preprocessor.invalid_timestamp_count)

    def test_writes_clean_csv(self):
        self.preprocessor.write_clean_csv('tiny_fake_dubious_data.csv')
        data = pd.read_csv('../test_data/tiny_fake_dubious_data.csv')
        # For this file, the clean version only has one valid timestamp
        self.assertEqual(2, len(data))

    def test_creates_image_directories(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('tiny_fake_dubious_data.csv')
        dirs = [self.preprocessor.data_dir + '/' + date for date in
                ['photos/20180418', 'photos/20180419', 'tsi_masks/20180418', 'tsi_masks/20180419']]
        # Destroy the existing directories
        for d in dirs:
            if os.path.isdir(d):
                shutil.rmtree(d)
        # Run the method
        self.preprocessor.create_image_directories('tiny_fake_dubious_data.csv')
        # Assert that the directories are present
        for d in dirs:
            self.assertTrue(os.path.isdir(d))

    def test_preprocesses_files(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('tiny_fake_dubious_data.csv')
        self.preprocessor.preprocess_images('tiny_fake_dubious_data.csv')
        files = [self.preprocessor.data_dir + '/photos/20180418/20180418000200_photo.jpg',
                 self.preprocessor.data_dir + '/photos/20180419/20180419000200_photo.jpg',
                 self.preprocessor.data_dir + '/tsi_masks/20180418/20180418000200_tsi_mask.png',
                 self.preprocessor.data_dir + '/tsi_masks/20180419/20180419000200_tsi_mask.png']
        for f in files:
            self.assertTrue(os.path.exists(f))

    def test_counts_images_per_date(self):
        # Ensure that the clean CSV file exists
        self.preprocessor.write_clean_csv('tiny_fake_dubious_data.csv')
        dates = self.preprocessor.count_images_per_date('tiny_fake_dubious_data.csv')
        correct = pd.DataFrame.from_dict({'date': ['20180418', '20180419'], 'count': [1, 1]})
        assert_frame_equal(correct, dates)

    def test_allocates_timestamps(self):
        # Make a shortcut to the real, raw typical csv file, pretending it's clean
        if not os.path.exists(self.preprocessor.data_dir + '/fake_clean_data.csv'):
            os.symlink(self.preprocessor.raw_csv_dir + '/shcu_typical_data.csv', self.preprocessor.data_dir + '/fake_clean_data.csv')
        filenames = ['typical_training_timestamps', 'typical_validation_timestamps', 'typical_testing_timestamps']
        self.preprocessor.allocate_timestamps('fake_clean_data.csv', [0.6, 0.2, 0.2], filenames)
        train = int(check_output(['wc', self.preprocessor.data_dir + '/typical_training_timestamps']).split()[0])
        valid = int(check_output(['wc', self.preprocessor.data_dir + '/typical_validation_timestamps']).split()[0])
        test = int(check_output(['wc', self.preprocessor.data_dir + '/typical_testing_timestamps']).split()[0])
        total = train + valid + test
        correct_total = int(check_output(['wc', self.preprocessor.data_dir + '/fake_clean_data.csv']).split()[0]) - 1
        self.assertEqual(correct_total, total)
        self.assertTrue(0.5 < train / total < 0.7)
        self.assertTrue(0.1 < valid / total < 0.3)
        self.assertTrue(0.1 < test / total < 0.3)


if __name__ == '__main__':
    unittest.main()
