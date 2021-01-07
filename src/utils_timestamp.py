"""
Utilities for dealing with timestamps, which are represented as strings in the format YYYYMMDDhhmmss.
"""

import random
import itertools

def hhmmss(timestamp):
    """
    Returns the substring of timestamp corresponding to the hour, minutes, and seconds.
    """
    return timestamp[8:]


def yyyymmdd(timestamp):
    """
    Returns the substring of timestamp corresponding to the year, month, and day.
    """
    return timestamp[:8]


def allocate_dates(dates, proportions):
    """
    Allocates dates randomly into multiple lists based on proportions.
    :param dates: a dictionary produced by Preprocessor.count_images_per_date
    :param proportions: a list of the fraction of timestamps in each category, e.g., [0.6, 0.2, 0.2]
    :return multiple lists of dates
    """
    shuffled = list(dates.keys())
    random.shuffle(shuffled)
    cumulative = list(itertools.accumulate([dates[d] for d in shuffled]))
    # TODO Finish this