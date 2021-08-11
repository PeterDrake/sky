from utils_image import *
import unittest
import numpy as np
from FscCalculator import *


class TestFscCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = FscCalculator('../test_network_masks')

    def test_counts_pixels(self):
        mask = np.array([[WHITE, BLUE], [WHITE, BLACK]])
        self.assertEqual([1, 0, 2], self.calculator.count_pixels(mask))

    def test_count_pixels_in_all_masks(self):
        stamps = ['20120501170000', '20120501170030', '20120501170100', '20120501170130']
        df = self.calculator.count_pixels_in_all_masks(stamps)
        print(df)
        print(df.sum(axis=1))