import unittest
from BatchGenerator import *


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
        for photo_batch, tsi_mask_batch in self.generator:
            self.assertEquals((32, 480, 480, 3), photo_batch.shape)
            self.assertEquals((32, 480, 480, 1), tsi_mask_batch.shape)

    def test_photo_appears_in_batch(self):
        # Arbitrarily choose the timestamp with index 3
        t = self.timestamps[3]
        photo_path = self.generator.data_dir + '/photos/' + yyyymmdd(t) + '/' + t + '_photo.jpg'
        photo = plt.imread(photo_path)
        photo_batch, _ = self.generator[0]  # Photo 3 should be in batch 0
        self.assertTrue((photo == photo_batch[3]).all())


if __name__ == '__main__':
    unittest.main()
