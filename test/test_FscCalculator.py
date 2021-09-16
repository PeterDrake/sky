from utils_image import *
import unittest
import numpy as np
from FscCalculator import *
import pandas as pd


class TestFscCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = FscCalculator('../test_network_masks', '../test_network_masks', '../test_results/test_experiment')

    def test_counts_pixels(self):
        mask = np.array([[WHITE, BLUE], [WHITE, BLACK]])
        self.assertEqual([1, 0, 2], self.calculator.count_pixels(mask))

    def test_counts_pixels_in_all_masks(self):
        stamps = ['20120501170000', '20120501170030', '20120501170100', '20120501170130']
        df = self.calculator.count_pixels_in_all_masks(stamps)
        self.assertEqual(22295, df['opaque_160']['20120501170030'])  # The number of opaque pixels in this image

    def test_saves_pixel_counts(self):
        timestamp_filename = 'typical_validation_timestamps'
        output_filename = 'network_fsc.csv'
        self.calculator.write_pixel_counts(timestamp_filename, output_filename)
        df = pd.read_csv(self.calculator.output_dir + '/' + output_filename, index_col=0)
        df.index = df.index.map(str)  # Converts the index values from int64 to str
        self.assertEqual(22295, df['opaque_160']['20120501170030'])  # The number of opaque pixels in this image
