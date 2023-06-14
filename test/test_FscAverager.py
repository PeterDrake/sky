import unittest
import numpy as np
import pandas as pd

from FscAverager import *


class TestFscAverager(unittest.TestCase):

    def setUp(self):
        self.averager = FscAverager('../test_raw_data', 'tiny_tsi_fsc.csv', half_width=1, min_stamps=3)

    def test_computes_averages(self):
        averages = self.averager.compute_averages(2012)
        self.assertEqual(12, len(averages))
        self.assertEqual('20120519120000', averages['timestamp_utc'][0])
        thins = 4278 + 3927 + 979
        totals = 36482 + 4278 + 12053 + 33578 + 3927 + 15412 + 38843 + 979 + 436
        self.assertEqual(thins / totals, averages['fsc_thin_100'][0])

    def test_saves_averages(self):
        self.averager.write_averages('tiny_tsi_fsc_2avg.csv')
        df = pd.read_csv('../test_raw_data/tiny_tsi_fsc_2avg.csv')
        self.assertEqual(17, len(df))
        self.assertEqual(20130519120200, df['timestamp_utc'][16])
