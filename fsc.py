#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finds the zenith area of TSI skymasks
"""

import numpy as np
from PIL import Image
from scipy import misc

def get_mask(timestamp):
    return np.array(misc.imread('data/simplemask/simplemask' + str(timestamp) + '.png'))

def show_skymask(timestamp):
    mask = get_mask(timestamp)
    mask_image = Image.fromarray(mask.astype('uint8'))
    mask_image.show()

# numpy array (480, 480, 3) go through find first non black pixel
def find_first_non_black_pixel(timestamp):
    mask = get_mask(timestamp)
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if tuple(mask[i, j]) != (0, 0, 0):
                print(i, j)
                return i, j

def find_second_non_black_pixel(timestamp):
    mask = get_mask(timestamp)
    print(mask[0])
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]-1, -1, -1):
            if tuple(mask[i, j]) != (0, 0, 0):
                print(mask.shape[0]-i, j)
                return i, j

    # for index, x in np.ndenumerate(mask):
    #
    # #black = 3
    #
    # # top
    # for i in np.nditer():
    #     if
    #
    #         img = misc.imread('simplemask/' + file)
    #         b_mask[(img != color).any(axis=2)] = BLUE

#preproccess.py simplify_all_masks to get all skymasks

if __name__ == '__main__':
    timestamp = 20160414162830
    show_skymask(timestamp)
    find_first_non_black_pixel(timestamp)
    find_second_non_black_pixel(timestamp)
