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


def crop(image, center_and_radius):
    """
    Returns a version of image cropped to 480x480, centered on the specified center.
    :param center_and_radius: (r, c), radius, as returned by center_and_radius
    """
    (r, c), _ = center_and_radius
    # Pad with zeroes (black) in case circle spills out of 480x480 region
    padded = np.pad(image, ((100, 100), (100, 100), (0, 0)))
    return padded[r-140:r+340, c-140:c+340]


def blacken_outer_ring(photo, center_and_radius):
    """
    Returns a version of photo with all pixels beyond radius away from center colored black.
    :param photo: 480x480x3 numpy array
    :param center_and_radius: (r, c), radius, as returned by center_and_radius
    """
    _, radius = center_and_radius
    circle = np.fromfunction(lambda r, c, _: (r - 240) ** 2 + (c - 240) ** 2 <= radius ** 2, (480, 480, 3))
    black = np.full((480, 480, 3), (0, 0, 0))  # TODO This should be a constant
    return np.where(circle, photo, black)
