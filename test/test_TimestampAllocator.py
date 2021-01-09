import unittest
import os
from pandas.testing import assert_frame_equal
from subprocess import check_output
from TimestampAllocator import *
from config import *


class TestTimestampAllocator(unittest.TestCase):
    
    def setUp(self):
        self.allocator = TimestampAllocator('../test_data', [0.6, 0.2, 0.2], verbose=True)
        
    def test_counts_images_per_date(self):
        # Make a shortcut to the real, raw typical csv file, pretending it's clean
        if not os.path.exists(self.allocator.data_dir + '/fake_clean_data.csv'):
            os.symlink(RAW_CSV_DIR + '/shcu_typical_data.csv', self.allocator.data_dir + '/fake_clean_data.csv')
        dates = self.allocator.count_images_per_date('fake_clean_data.csv')
        self.assertEqual(858, dates.loc[dates['date'] == '20120501', 'count'][0])

    def test_allocates_timestamps(self):
        # Make a shortcut to the real, raw typical csv file, pretending it's clean
        if not os.path.exists(self.allocator.data_dir + '/fake_clean_data.csv'):
            os.symlink(RAW_CSV_DIR + '/shcu_typical_data.csv', self.allocator.data_dir + '/fake_clean_data.csv')
        self.allocator.allocate_timestamps('fake_clean_data.csv', True)
        train = int(check_output(['wc', self.allocator.data_dir + '/typical_training_timestamps']).split()[0])
        valid = int(check_output(['wc', self.allocator.data_dir + '/typical_validation_timestamps']).split()[0])
        test = int(check_output(['wc', self.allocator.data_dir + '/typical_testing_timestamps']).split()[0])
        total = train + valid + test
        correct_total = int(check_output(['wc', self.allocator.data_dir + '/fake_clean_data.csv']).split()[0]) - 1
        self.assertEqual(correct_total, total)
        self.assertTrue(0.5 < train / total < 0.7)
        self.assertTrue(0.1 < valid / total < 0.3)
        self.assertTrue(0.1 < test / total < 0.3)

