"""
Utilities for dealing with timestamps, which are represented as strings in the format YYYYMMDDhhmmss.
"""
from itertools import accumulate


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


def allocate_dates(date_counts, proportions):
    """
    Allocates dates randomly into multiple lists based on proportions.
    :param date_counts: a dataframe produced by Preprocessor.count_images_per_date
    :param proportions: a list of the fraction of timestamps in each category, e.g., [0.6, 0.2, 0.2]
    :return a list of lists of dates
    """
    # Shuffle the rows
    date_counts = date_counts.sample(frac=1).reset_index(drop=True)
    # Add a column showing cumulative sum of counts
    date_counts['cum_count'] = date_counts['count'].cumsum()
    # Determine cutoffs
    total_count = date_counts['count'].sum()
    cutoffs = [c * total_count for c in accumulate(proportions)]
    # Take subsets based on those cutoffs
    paired_cutoffs = zip([0] + cutoffs[:-1], cutoffs)
    subsets = [date_counts[(lower < date_counts['cum_count']) & (date_counts['cum_count'] <= upper)]['date'] for lower, upper in paired_cutoffs]
    return [list(s) for s in subsets]


def timestamp_to_photo_path(dir, timestamp):
    """
    Returns the full path for the photo file for timestamp in dir.
    """
    return dir + '/photos/' + yyyymmdd(timestamp) + '/' + timestamp + '_photo.jpg'


def timestamp_to_tsi_mask_path(dir, timestamp):
    """
    Returns the full path for the TSI mask file for timestamp in dir.
    """
    return dir + '/tsi_masks/' + yyyymmdd(timestamp) + '/' + timestamp + '_tsi_mask.png'


def timestamp_to_network_mask_path(dir, timestamp):
    """
    Returns the full path for the network mask file for timestamp in dir.
    """
    return dir + '/network_masks/' + yyyymmdd(timestamp) + '/' + timestamp + '_network_mask.png'
