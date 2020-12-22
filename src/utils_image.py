"""
Utilities for dealing with images.
"""


def circle_edges(image):
    """
    Returns the indices of the top, bottom, left, and right of the box bounding the non-black region of image.
    (In a TSI mask, the non-black region is roughly circular.)
    """
    rows = image.max(axis=(1, 2)).nonzero()[0]
    columns = image.max(axis=(0, 2)).nonzero()[0]
    return rows[0], rows[-1], columns[0], columns[-1]
