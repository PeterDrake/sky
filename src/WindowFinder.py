from datetime import datetime, timedelta
from bisect import *

class WindowFinder:
    """
    Finds 15-minute windows of timestamps centered on each TSI image timestamp.
    """

    def __init__(self, timestamp_filename, half_width=7.5, min_stamps=25):
        # It is assumed that the timestamps in the file are sorted!
        with open(timestamp_filename, 'r') as f:
            self.stamps = [line.strip() for line in f.readlines()]
        self.half_width = half_width  # width of the window (in minutes)
        self.min_stamps = min_stamps  # minimum number of stamps in each window

    def years(self):
        """
        Returns a list of the years that appear in this WindowFinder's list of timestamps.
        """
        return sorted(list(set(s[:4] for s in self.stamps)))

    def first_and_last_timestamps(self, year):
        """
        Returns the first timestamp in year within this WindowFinder's list of timestamps.
        """
        for s in self.stamps:
            if s.startswith(year):
                first = s
                break
        for s in reversed(self.stamps):
            if s.startswith(year):
                last = s
                break
        return first, last

    def find_initial_boundaries(self, stamp):
        """
        Returns the timestamps that are before and after stamp by the amount specified by self.half_width.
        """
        dt = datetime.strptime(stamp, '%Y%m%d%H%M%S')
        delta = timedelta(minutes=self.half_width)
        return (dt - delta).strftime('%Y%m%d%H%M%S'), (dt + delta).strftime('%Y%m%d%H%M%S')

    def find_initial_window(self, stamp):
        """
        Returns the indices of the first and last timestamps that are within HALF_WIDTH of stamp.
        """
        first_stamp, last_stamp = self.find_initial_boundaries(stamp)
        first_index = bisect_left(self.stamps, first_stamp)
        last_index = bisect_left(self.stamps, last_stamp)
        return first_index, last_index

    def find_windows(self, year):
        """
        Returns a dictionary associating valid timestamp centers with pairs of indices into self.stamps indicating
        the boundaries of the corresponding windows.
        """
        center = self.first_timestamp(year)
        first_stamp, last_stamp = self.find_initial_boundaries(center)
        first_index, last_index = self.find_initial_window(center)

