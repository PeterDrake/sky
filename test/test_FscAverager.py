import unittest
from datetime import datetime

from FscAverager import *

def p(stamp):
    """
    Convenience method to turn a human-readable timestamp string into a datetime.
    """
    return datetime.strptime(stamp, '%Y%m%d%H%M%S')

class TestFscAverager(unittest.TestCase):

    def setUp(self):
        self.averager = FscAverager('../test_raw_csv', 'tiny_tsi_fsc.csv')

    def test_finds_years(self):
        self.assertEqual([2016, 2017], self.averager.years())

    def test_finds_first_and_last_times(self):
        self.assertEqual((p('20170524150000'), p('20170524193000')), self.averager.first_and_last_times(2017))

    def test_finds_initial_boundaries(self):
        self.assertEqual((p('20150510200730'), p('20150510202230')),
                         self.averager.find_initial_boundaries(p('20150510201500')))

    def test_finds_initial_window(self):
        self.assertEqual((5, 13),
                         self.averager.find_initial_window(p('20170524150000')))

    def test_finds_windows(self):
        averager = FscAverager('../test_raw_csv', 'tiny_tsi_fsc.csv', half_width=1, min_stamps=3)
        correct = {'20170524150000': (5, 7),
                   '20170524150030': (5, 8),
                   '20170524150100': (5, 9),
                   '20170524150130': (6, 9),
                   '20170524150200': (7, 10),
                   '20170524150300': (9, 12),
                   '20170524150330': (10, 13),
                   '20170524150400': (10, 13),
                   '20170524150430': (11, 13),
                   '20170524173000': (14, 16),
                   '20170524173030': (14, 16),
                   '20170524173100': (14, 16)}
        self.assertEqual(correct, averager.find_windows(2017))

    def test_computes_averages(self):
        averager = FscAverager('../test_raw_csv', 'tiny_tsi_fsc.csv', half_width=1, min_stamps=3)
        averages = averager.compute_averages(2016)
        self.assertEqual(5, len(averages))
        self.assertEqual('20160525160000', averages['timestamp_utc'][0])
        thins = 633 + 1601 + 6067
        totals = 37 + 633 + 41866 + 13 + 1601 + 40922 + 37 + 6067 + 36340
        self.assertEqual(thins / totals, averages['fsc_thin_100'][0])

    def test_saves_averages(self):
        averager = FscAverager('../test_raw_csv', 'tiny_tsi_fsc.csv', half_width=1, min_stamps=3)
        averager.write_averages('tiny_tsi_fsc_2avg.csv')
        df = pd.read_csv('../test_raw_csv/tiny_tsi_fsc_2avg.csv')
        self.assertEqual(17, len(df))
        self.assertEqual(20170524173100, df['timestamp_utc'][16])
