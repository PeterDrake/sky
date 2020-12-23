"""
Utilities for dealing with images.
"""

import numpy as np


def circle_edges(mask):
    """
    Returns the indices of the top, bottom, left, and right of the box bounding the non-black region of mask.
    (In a TSI mask, the non-black region is roughly circular.)
    """
    rows = mask.max(axis=(1, 2)).nonzero()[0]
    columns = mask.max(axis=(0, 2)).nonzero()[0]
    return rows[0], rows[-1], columns[0], columns[-1]


def center_and_radius(mask):
    """
    Returns the center of the non-black region of mask as a pair (r, c) as well as the radius of the non-black
    region (averaged between vertical and horizontal.
    """
    top, bottom, left, right = circle_edges(mask)
    vertical_radius = (bottom - top) / 2
    horizontal_radius = (right - left) / 2
    return (int((top + bottom) / 2),
            int((left + right) / 2)),\
           (vertical_radius + horizontal_radius) / 2


def crop_mask(mask, center_and_radius):
    """
    Returns a version of mask cropped to 480x480, centered on the specified center.
    :param center_and_radius: (r, c), radius, as returned by center_and_radius
    """
    (r, c), _ = center_and_radius
    # Pad with zeroes (black) in case circle spills out of 480x480 region
    padded = np.pad(mask, ((100, 100), (100, 100), (0, 0)))
    return padded[r-140:r+340, c-140:c+340]


def crop_photo_and_add_border(photo, center_and_radius):
    pass