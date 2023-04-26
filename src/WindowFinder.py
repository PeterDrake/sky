class WindowFinder:
    """
    Finds 15-minute windows of timestamps centered on each TSI image timestamp.
    """

    def __init__(self, timestamp_filename):
        with open(timestamp_filename, 'r') as f:
            self.stamps = [line.strip() for line in f.readlines()]

    def years(self):
        """
        Returns a list of the years that appear in this WindowFinder's list of timestamps.
        """
        return sorted(list(set(s[:4] for s in self.stamps)))
