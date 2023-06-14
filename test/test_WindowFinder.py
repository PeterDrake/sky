import unittest
from WindowFinder import *


def p(stamp):
    """
    Convenience method to turn a human-readable timestamp string into a datetime.
    """
    return datetime.strptime(stamp, '%Y%m%d%H%M%S')


class TestWindowFinder(unittest.TestCase):

    def setUp(self):
        self.window_finder = WindowFinder('../test_raw_data/tiny_tsi_fsc.csv')

    def test_finds_years(self):
        self.assertEqual([2012, 2013], self.window_finder.years())

    def test_finds_first_and_last_times(self):
        self.assertEqual((p('20130519120000'), p('20130519120200')), self.window_finder.first_and_last_times(2013))

    def test_finds_initial_boundaries(self):
        self.assertEqual((p('20150510200730'), p('20150510202230')),
                         self.window_finder.find_initial_boundaries(p('20150510201500')))

    def test_finds_initial_window(self):
        self.assertEqual((0, 8),
                         self.window_finder.find_initial_window(p('20120519120000')))

    def test_finds_windows(self):
        window_finder = WindowFinder('../test_raw_data/tiny_tsi_fsc.csv', half_width=1, min_stamps=3)
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
        self.assertEqual(correct, window_finder.find_windows(2012))
