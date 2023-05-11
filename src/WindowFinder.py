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
        year = str(year)
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
        result = {}
        center_stamp, final_stamp = self.first_and_last_timestamps(year)
        first_stamp, last_stamp = self.find_initial_boundaries(center_stamp)
        first_index, last_index = self.find_initial_window(center_stamp)
        # TODO We could avoid this if we had a list of datetimes instead of (or in addition to) self.stamps
        center_stamp = datetime.strptime(center_stamp, '%Y%m%d%H%M%S')
        final_stamp = datetime.strptime(final_stamp, '%Y%m%d%H%M%S')
        first_stamp = datetime.strptime(first_stamp, '%Y%m%d%H%M%S')
        last_stamp = datetime.strptime(last_stamp, '%Y%m%d%H%M%S')
        while center_stamp <= final_stamp:
            if (last_index - first_index + 1 >= self.min_stamps) and\
                    (center_stamp.strftime('%Y%m%d%H%M%S') in self.stamps[first_index:last_index+1]):
                result[center_stamp.strftime('%Y%m%d%H%M%S')] = (first_index, last_index)
            if datetime.strptime(self.stamps[first_index], '%Y%m%d%H%M%S') == first_stamp:
                first_index += 1
            first_stamp += timedelta(minutes=0.5)  # TODO This should be a constant
            last_stamp += timedelta(minutes=0.5)
            # print("Trying to add " + )
            if datetime.strptime(self.stamps[last_index + 1], '%Y%m%d%H%M%S') == last_stamp:
                last_index += 1
            center_stamp += timedelta(minutes=0.5)
        return result