import unittest
from BatchGenerator import *
import pandas as pd
from skimage.io import imsave, imread
# from test import test_Preprocessor


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # Make up some timestamps
        timestamps = pd.read_csv('../test_data/tiny_data.csv', converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
        timestamps = timestamps['timestamp_utc'].tolist()
        self.timestamps = timestamps[:96]
        # Initialize the generator
        self.generator = BatchGenerator(self.timestamps, '../test_data')

    def test_has_correct_length(self):
        self.assertEqual(3, len(self.generator))

    def test_outputs_have_correct_dimensions(self):
        print('NOTE: This will fail if test_Preprocessor has not run yet. If you are running all of the tests on a')
        print('fresh install, just wait for them to finish and run them all again.')
        for photo_batch, tsi_mask_batch in self.generator:
            self.assertEqual((32, 480, 480, 3), photo_batch.shape)
            self.assertEqual((32, 480, 480, 1), tsi_mask_batch.shape)

    def test_photo_appears_in_batch(self):
        print('NOTE: This will fail if test_Preprocessor has not run yet. If you are running all of the tests on a')
        print('fresh install, just wait for them to finish and run them all again.')
        # Arbitrarily choose the timestamp with index 3
        t = self.timestamps[3]
        photo_path = timestamp_to_photo_path(self.generator.data_dir, t)
        photo = imread(photo_path)
        photo_batch, _ = self.generator[0]  # Photo 3 should be in batch 0
        self.assertTrue((photo == photo_batch[3]).all())


if __name__ == '__main__':
    unittest.main()
