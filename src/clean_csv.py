RAW_DATA_DIR = "/home/users/jkleiss/TSI_C1"

def timestamp_to_yyyymmdd(timestamp):
    return timestamp[:8]

def raw_photo_path(timestamp):
    """Returns the path of a raw photo file."""
    result = RAW_DATA_DIR + '/SkyImage/'
    import glob
    dir = glob.glob(result + 'sgptsiskyimageC1.a1.' + timestamp_to_yyyymmdd(timestamp) + '.*')
    print(dir)
    # TODO Still need to add specific file name

def photo_exists(image_name):
    """
    Returns True iff a raw (unpreprocessed), nonempty photo exists with image_name.
    """
    pass

if __name__ == "__main__":
    raw_photo_path('20180419010230')