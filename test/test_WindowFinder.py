import unittest
from WindowFinder import *


class TestWindowFinder(unittest.TestCase):

    def setUp(self):
        self.window_finder = WindowFinder('../test_data/typical_validation_timestamps')

    def test_finds_years(self):
        self.assertEqual(['2012', '2013', '2014', '2015', '2016', '2017'], self.window_finder.years())

    def test_finds_first_timestamp(self):
        self.assertEqual('20150510201500', self.window_finder.first_timestamp('2015'))

    def test_finds_initial_boundaries(self):
        self.assertEqual(('20150510200730', '20150510202230'),
                         self.window_finder.find_initial_boundaries('20150510201500'))

    def test_finds_initial_window(self):
        self.assertEqual((10947, 10962),
                         self.window_finder.find_initial_window('20150510201500'))

    def test_finds_windows(self):
        window_finder = WindowFinder('../test_raw_data/tiny_timestamps', half_width=1, min_stamps=3)
        correct = {'20120519120000': (0, 2),
                   '20120519120030': (0, 3),
                   '20120519120100': (0, 4),
                   '20120519120130': (1, 4),
                   '20120519120200': (2, 5),
                   '20120519120300': (4, 7),
                   '20120519120330': (5, 8),
                   '20120519120400': (6, 8),
                   '20120519140000': (9, 11),
                   '20120519140030': (9, 11),
                   '20120519140100': (9, 11)}
        self.assertEqual(correct, window_finder.find_windows(2012))
