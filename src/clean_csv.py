from config import *
from utils_timestamp import *


def raw_photo_path(timestamp):
    """Returns the path of a raw photo file, or None if there is no such file."""
    result = RAW_DATA_DIR + '/SkyImage/'
    import glob
    dirs = glob.glob(result + 'sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '.*')
    if not dirs:
        return None
    dir = dirs[0]
    return dir + '/sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '.' + hhmmss(timestamp) + '.jpg.' + timestamp + '.jpg'


def photo_exists(image_name):
    """
    Returns True iff a nonempty raw photo exists with image_name.
    """
    pass


if __name__ == "__main__":
    raw_photo_path('20180419010230')