from utils_image import *
import unittest
import numpy as np
from FscCalculator import *


class TestFscCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = FscCalculator()

    def test_counts_pixels(self):
        image = np.array([[WHITE, BLUE], [WHITE, BLACK]])
        self.assertEqual(2, self.calculator.count_pixels(image, WHITE))
