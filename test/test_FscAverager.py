import unittest

from FscAverager import *

def p(stamp):
    """
    Convenience method to turn a human-readable timestamp string into a datetime.
    """
    return datetime.strptime(stamp, '%Y%m%d%H%M%S')

class TestFscAverager(unittest.TestCase):

    def setUp(self):
        self.averager = FscAverager('../test_raw_data', 'tiny_tsi_fsc.csv')

    def test_finds_years(self):
        self.assertEqual([2012, 2013], self.averager.years())

    def test_finds_first_and_last_times(self):
        self.assertEqual((p('20130519120000'), p('20130519120200')), self.averager.first_and_last_times(2013))

    def test_finds_initial_boundaries(self):
        self.assertEqual((p('20150510200730'), p('20150510202230')),
                         self.averager.find_initial_boundaries(p('20150510201500')))

    def test_finds_initial_window(self):
        self.assertEqual((0, 8),
                         self.averager.find_initial_window(p('20120519120000')))

    def test_finds_windows(self):
        averager = FscAverager('../test_raw_data', 'tiny_tsi_fsc.csv', half_width=1, min_stamps=3)
        correct = {'20120519120000': (0, 2),
                   '20120519120030': (0, 3),
                   '20120519120100': (0, 4),
                   '20120519120130': (1, 4),
                   '20120519120200': (2, 5),
                   '20120519120300': (4, 7),
                   '20120519120330': (5, 8),
                   '20120519120400': (5, 8),
                   '20120519120430': (6, 8),
                   '20120519140000': (9, 11),
                   '20120519140030': (9, 11),
                   '20120519140100': (9, 11)}
        self.assertEqual(correct, averager.find_windows(2012))

    def test_computes_averages(self):
        averager = FscAverager('../test_raw_data', 'tiny_tsi_fsc.csv', half_width=1, min_stamps=3)
        averages = averager.compute_averages(2012)
        self.assertEqual(12, len(averages))
        self.assertEqual('20120519120000', averages['timestamp_utc'][0])
        thins = 4278 + 3927 + 979
        totals = 36482 + 4278 + 12053 + 33578 + 3927 + 15412 + 38843 + 979 + 436
        self.assertEqual(thins / totals, averages['fsc_thin_100'][0])

    def test_saves_averages(self):
        averager = FscAverager('../test_raw_data', 'tiny_tsi_fsc.csv', half_width=1, min_stamps=3)
        averager.write_averages('tiny_tsi_fsc_2avg.csv')
        df = pd.read_csv('../test_raw_data/tiny_tsi_fsc_2avg.csv')
        self.assertEqual(17, len(df))
        self.assertEqual(20130519120200, df['timestamp_utc'][16])
