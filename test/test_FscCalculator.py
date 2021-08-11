from utils_image import *
import unittest
import numpy as np
from FscCalculator import *


class TestFscCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = FscCalculator()

    def test_counts_pixels(self):
        mask = np.array([[WHITE, BLUE], [WHITE, BLACK]])
        self.assertEqual([1, 0, 2], self.calculator.count_pixels(mask))
