import unittest
from WindowFinder import *


class TestPreprocessor(unittest.TestCase):

    def setUp(self):
        self.window_finder = WindowFinder('../test_data/typical_validation_timestamps')

    def test_finds_years(self):
        self.assertEqual(['2012', '2013', '2014', '2015', '2016', '2017'], self.window_finder.years())
