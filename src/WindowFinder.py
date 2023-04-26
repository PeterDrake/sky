from datetime import datetime, timedelta

class WindowFinder:
    """
    Finds 15-minute windows of timestamps centered on each TSI image timestamp.
    """

    # Set the width of the window (in minutes)
    HALF_WIDTH = 7.5

    def __init__(self, timestamp_filename):
        # It is assumed that the timestamps in the file are sorted!
        with open(timestamp_filename, 'r') as f:
            self.stamps = [line.strip() for line in f.readlines()]

    def years(self):
        """
        Returns a list of the years that appear in this WindowFinder's list of timestamps.
        """
        return sorted(list(set(s[:4] for s in self.stamps)))

    def first_timestamp(self, year):
        """
        Returns the first timestamp in year within this WindowFinder's list of timestamps.
        """
        for s in self.stamps:
            if s.startswith(year):
                return s

    def find_begin_time(self, stamp):
        """
        Returns a timestamp that is before stamp by the amount specified by HALF_WIDTH.
        """
        dt = datetime.strptime(stamp, '%Y%m%d%H%M%S')
        start = dt - timedelta(minutes=WindowFinder.HALF_WIDTH)
        return start.strftime('%Y%m%d%H%M%S')

