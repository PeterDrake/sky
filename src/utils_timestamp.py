"""
Utilities for dealing with timestamps, which are represented as strings in the format YYYYMMDDhhmmss.
"""


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


