from datetime import datetime, timedelta
from bisect import *
import pandas as pd


class WindowFinder:
    """
    Finds 15-minute windows of timestamps centered on each TSI image timestamp.
    """

    THIRTY_SECONDS = timedelta(minutes=0.5)

    def __init__(self, csv_filename, half_width=7.5, min_stamps=25):
        # It is assumed that the timestamps in the file are sorted!
        self.stamps = list(pd.read_csv(csv_filename, usecols=['timestamp_utc'], dtype=str)['timestamp_utc'])
        self.times = [datetime.strptime(s, '%Y%m%d%H%M%S') for s in self.stamps]
        self.half_width = half_width  # width of the window (in minutes)
        self.min_stamps = min_stamps  # minimum number of stamps in each window

    def years(self):
        """
        Returns a list of the years that appear in this WindowFinder's list of timestamps.
        """
        return sorted(list(set(int(s[:4]) for s in self.stamps)))

    def first_and_last_times(self, year):
        """
        Returns the first and last time in year within self.times.
        """
        for t in self.times:
            if t.year == year:
                first = t
                break
        for t in reversed(self.times):
            if t.year == year:
                last = t
                break
        return first, last

    def find_initial_boundaries(self, time):
        """
        Returns the times that are before and after time by the amount specified by self.half_width.
        """
        delta = timedelta(minutes=self.half_width)
        return (time - delta), (time + delta)

    def find_initial_window(self, time):
        """
        Returns the indices of the first and last timestamps that are within self.half_width of time.
        """
        first_time, last_time = self.find_initial_boundaries(time)
        first_index = bisect_left(self.times, first_time)
        last_index = bisect_left(self.times, last_time)
        # If last_time isn't present, bisect_left will find the index AFTER the window.
        # The following line corrects for this
        if self.times[last_index] != last_time:
            last_index -= 1
        return first_index, last_index

    def find_windows(self, year):
        """
        Returns a dictionary associating valid timestamp centers with pairs of indices into self.stamps indicating
        the boundaries of the corresponding windows.
        """
        result = {}
        center_time, final_time = self.first_and_last_times(year)
        first_time, last_time = self.find_initial_boundaries(center_time)
        first_index, last_index = self.find_initial_window(center_time)
        while center_time <= final_time:
            if (last_index - first_index + 1 >= self.min_stamps) and\
                    (center_time.strftime('%Y%m%d%H%M%S') in self.stamps[first_index:last_index+1]):
                result[center_time.strftime('%Y%m%d%H%M%S')] = (first_index, last_index)
            if self.times[first_index] == first_time:
                first_index += 1
            first_time += WindowFinder.THIRTY_SECONDS
            last_time += WindowFinder.THIRTY_SECONDS
            if self.times[last_index + 1] == last_time:
                last_index += 1
            center_time += WindowFinder.THIRTY_SECONDS
        return result