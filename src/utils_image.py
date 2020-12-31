"""
Utilities for dealing with images.
"""

import numpy as np
import skimage.color
import skimage.measure
import skimage.segmentation
import matplotlib.pyplot as plt

# Colors used in masks - DO NOT TOUCH
WHITE = np.array([255, 255, 255], dtype=np.uint8)
BLUE = np.array([0, 0, 255], dtype=np.uint8)
GRAY = np.array([192, 192, 192], dtype=np.uint8)
BLACK = np.array([0, 0, 0], dtype=np.uint8)
GREEN = np.array([0, 255, 0], dtype=np.uint8)
YELLOW = np.array([255, 255, 0], dtype=np.uint8)
COLORS = (WHITE, BLUE, GRAY, BLACK, GREEN)

CROPPED_BLACK_IMAGE = np.full((480, 480, 3), BLACK)

TRUES_480_480 = np.ones((480, 480), dtype=bool)
FALSES_480_480 = np.zeros((480, 480), dtype=bool)


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
    :param image 640480x3 image
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
    return np.where(circle, photo, CROPPED_BLACK_IMAGE)


def remove_sun(mask):
    """
    Returns a version of mask with the sun removed. The sun is either a region of yellow pixels or a region of
    white pixels surrounded by black pixels. NOTE: While this never happens in our data, you might have cases
    where the camera arm and shadowband bound a small sliver of thick cloud that this algorithm will see as the
    sun. If you are concerned about this, modify the end of this function to count the suns and report any masks
    with more than one sun.
    """
    yellow_pixels = (mask == YELLOW).all(axis=2)
    if yellow_pixels.any():
        mask[yellow_pixels] = BLACK
        return mask
    else:
        # Make the whole sky thick cloud to reduce the number of segments
        overcast = np.copy(mask)
        overcast[(mask == BLUE).all(axis=2)] = WHITE
        overcast[(mask == GRAY).all(axis=2)] = WHITE
        # Convert the image to grayscale
        # TODO Once we have a function to convert RGB to mask color numbers, use that here
        gray = skimage.color.rgb2gray(overcast) * 255
        # Segment the mask
        labels, n = skimage.measure.label(gray, connectivity=1, return_num=True)
        # For each segment
        for label in range(1, n + 1):
            region = np.where((labels == label) & (gray == 255), TRUES_480_480, FALSES_480_480)
            # If this region is non-white, it's now empty
            if region.any():  # If this region is not empty ...
                boundary = skimage.segmentation.find_boundaries(region, mode='outer')
                if (gray[boundary] == 0).all():  # ... and it's surrounded by black
                    # This one is the sun!
                    mask[region] = BLACK
                    return mask
