#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finds the zenith area of TSI skymasks
"""

import numpy as np
from PIL import Image
from scipy import misc

def show_skymask(timestamp):
    mask = np.array(misc.imread('data/simplemask/simplemask' + str(timestamp) + '.png'))
    mask_image = Image.fromarray(mask.astype('uint8'))
    mask_image.show()

if __name__ == '__main__':
    timestamp = 20160601134530
    show_skymask(timestamp)
