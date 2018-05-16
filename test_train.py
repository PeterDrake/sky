#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:51:32 2017

@author: jeffmullins
"""


import unittest
from preprocess import WHITE, BLUE, GRAY, BLACK, GREEN
import train
import numpy as np


class Test_train(unittest.TestCase):

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_mask_to_index(self):
        img = np.array([[BLACK, WHITE, BLUE],
                        [GRAY, GREEN, WHITE],
                        [BLUE, WHITE, WHITE]])
        indexes = train.mask_to_index(img)
        correct = np.array([[3, 0, 1],
                            [2, 4, 0],
                            [1, 0, 0]])
        self.assertTrue((indexes == correct).all())

    def test_color_mask(self):
        img = np.array([[BLUE, WHITE],
                        [WHITE, WHITE]])
        mask = train.color_mask(img, 2)
        correct = np.array([[[0, 0, 0, 0, 0], [0, 0, 1e7, 0, 0]],
                            [[0, 0, 1e7, 0, 0], [0, 0, 1e7, 0, 0]]])
        self.assertTrue((mask == correct).all())


if __name__ == '__main__':
    unittest.main()
