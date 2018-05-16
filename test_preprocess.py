#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 10:45:02 2017

@author: drake
"""

from preprocess import BLACK, BLUE, GREEN, YELLOW, WHITE, GRAY
import numpy as np
import unittest
from preprocess import simplify_name, extract_timestamp, separate_stamps, remove_white_sun, count_colors


class TestPreprocess(unittest.TestCase):

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_simplify_name_skyimage(self):
        f = 'sgptsiskyimageC1.a1.20160414.235930.jpg.20160414235930.jpg'
        self.assertEqual(simplify_name(f), 'skyimage20160414235930.jpg')

    def test_simplify_name_cldmask(self):
        f = 'sgptsicldmaskC1.a1.20160414.235930.png.20160414235930.png'
        self.assertEqual(simplify_name(f), 'cldmask20160414235930.png')

    def test_extract_timestamp(self):
        f = 'sgptsicldmaskC1.a1.20160414.235930.png.20160414235930.png'
        self.assertEqual(extract_timestamp(f), '20160414235930')
        
    def test_remove_white_sun(self):
        img = np.array([[BLACK, BLUE, BLACK, BLACK, BLACK, BLACK, BLACK],
                       [BLACK, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK],
                       [BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, BLACK],
                       [BLACK, BLUE, BLACK, WHITE, WHITE, BLACK, BLACK],
                       [BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, BLACK],
                       [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
                       [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]])
        correct = np.array([[BLACK, BLUE,  BLACK, BLACK, BLACK, BLACK, BLACK],
                            [BLACK, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK],
                            [BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, BLACK],
                            [BLACK, BLUE,  BLACK, BLACK, BLACK, BLACK, BLACK],
                            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
                            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
                            [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]])
        # correct = (2,2)
        out = remove_white_sun(img, stride=1)
        self.assertTrue((out == correct).all())

    def test_color_counts(self):
        img = np.array([[BLACK, BLUE, BLACK],
                        [WHITE, BLACK, WHITE]])
        probs = count_colors(img)
        correct = np.array([2, 1, 0, 3, 0])
        self.assertTrue((probs == correct).all())

    def test_separate_stamps(self):
        data = list(range(100))
        test, valid, train = separate_stamps(data)
        self.assertEqual(len(test), 20)
        self.assertEqual(len(valid), 16)
        self.assertEqual(len(train), 64)
        numbers = test + valid + train
        # This will fail in the rare event that shuffling does nothing
        self.assertNotEqual(numbers, list(range(100)))
        numbers.sort()  # For equality testing below
        self.assertEqual(numbers, list(range(100)))

if __name__ == '__main__':
    unittest.main()
