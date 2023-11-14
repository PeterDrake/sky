from utils_timestamp import *
import unittest
import pandas as pd


class TestUtilsTimestamp(unittest.TestCase):

    def test_extracts_yyyymmdd(self):
        self.assertEqual('20180419', yyyymmdd('20180419010230'))

    def test_extracts_hhmmss(self):
        self.assertEqual('010230', hhmmss('20180419010230'))

    def test_allocates_dates(self):
        days = [str(d) for d in range(100)]
        counts = ([1] * 70) + ([3] * 30)
        dates = pd.DataFrame.from_dict({'date': days, 'count': counts})
        train, test = allocate_dates(dates, [0.8, 0.2])
        total_count = sum(counts)
        train_count = dates[dates['date'].isin(train)].sum()['count']
        test_count = dates[dates['date'].isin(test)].sum()['count']
        self.assertTrue(0.75 < train_count / total_count < 0.85)
        self.assertTrue(0.15 < test_count / total_count < 0.25)

    def test_finds_photo_path(self):
        # Note: it doesn't matter if this file actually exists; we're just verifying that the correct path is returned
        self.assertEqual('../test_data/photos/20180419/20180419010230_photo.jpg', timestamp_to_photo_path('../test_data', '20180419010230'))

    def test_finds_tsi_mask_path(self):
        # Note: it doesn't matter if this file actually exists; we're just verifying that the correct path is returned
        self.assertEqual('../test_data/tsi_masks/20180419/20180419010230_tsi_mask.png', timestamp_to_tsi_mask_path('../test_data', '20180419010230'))

    def test_finds_tsi_mask_no_glare_path(self):
        # Note: it doesn't matter if this file actually exists; we're just verifying that the correct path is returned
        self.assertEqual('../test_data/tsi_masks_no_glare/20180419/20180419010230_tsi_mask.png', timestamp_to_tsi_mask_no_glare_path('../test_data', '20180419010230'))

    def test_finds_network_mask_path(self):
        # Note: it doesn't matter if this file actually exists; we're just verifying that the correct path is returned
        self.assertEqual('../test_results/sandbox/network_masks/20180419/20180419010230_network_mask.png', timestamp_to_network_mask_path('../test_results/sandbox', '20180419010230'))


if __name__ == '__main__':
    unittest.main()
