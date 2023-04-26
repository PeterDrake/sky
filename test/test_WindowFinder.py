import unittest
from WindowFinder import *


class TestWindowFinder(unittest.TestCase):

    def setUp(self):
        self.window_finder = WindowFinder('../test_data/typical_validation_timestamps')

    def test_finds_years(self):
        self.assertEqual(['2012', '2013', '2014', '2015', '2016', '2017'], self.window_finder.years())

    def test_finds_first_timestamp(self):
        self.assertEqual('20150510201500', self.window_finder.first_timestamp('2015'))

    def test_finds_begin_time(self):
        self.assertEqual('20150510200730', self.window_finder.find_begin_time('20150510201500'))