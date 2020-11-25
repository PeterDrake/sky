import os
from utils_timestamp import *


class Preprocessor:

    def __init__(self, raw_data_dir):
        self.raw_data_dir = raw_data_dir

    def raw_photo_path(self, timestamp):
        """Returns the path of a raw photo file, or None if there is no such file."""
        result = self.raw_data_dir + '/SkyImage/'
        import glob
        dirs = glob.glob(result + 'sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '.*')
        if not dirs:
            return None
        return dirs[0] + '/sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '.' + hhmmss(timestamp) + '.jpg.' + timestamp + '.jpg'

    def photo_exists(self, timestamp):
        """
        Returns True iff a nonempty raw photo exists for timestamp.
        """
        path = self.raw_photo_path(timestamp)
        return os.path.exists(path) and os.path.getsize(path) > 0
