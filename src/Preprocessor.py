import glob
import os
import pandas as pd
from utils_timestamp import *


class Preprocessor:

    def __init__(self, raw_data_dir, raw_csv_dir, data_dir):
        self.raw_data_dir = raw_data_dir
        self.raw_csv_dir = raw_csv_dir
        self.data_dir = data_dir
        self.valid_timestamp_count = 'Only meaningful if validate_csv has been called'
        self.invalid_timestamp_count = 'Only meaningful if validate_csv has been called'

    def raw_photo_path(self, timestamp):
        """Returns the path of a raw photo file, or None if there is no such file."""
        result = self.raw_data_dir + '/SkyImage/'
        dirs = glob.glob(result + 'sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '*')
        if not dirs:
            return None
        return dirs[0] + '/sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '.' + hhmmss(timestamp) + '.jpg.' + timestamp + '.jpg'

    def photo_exists(self, timestamp):
        """
        Returns True iff a nonempty raw photo exists for timestamp.
        """
        path = self.raw_photo_path(timestamp)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def raw_tsi_mask_path(self, timestamp):
        """Returns the path of a raw TSI mask file, or None if there is no such file."""
        result = self.raw_data_dir + '/CloudMask/'
        dir = result + 'sgptsicldmaskC1.a1.' + yyyymmdd(timestamp)
        if not os.path.exists(dir):
            return None
        return dir + '/sgptsicldmaskC1.a1.' + yyyymmdd(timestamp) + '.' + hhmmss(timestamp) + '.png.' + timestamp + '.png'

    def tsi_mask_exists(self, timestamp):
        """
        Returns True iff a nonempty raw TSI mask exists for timestamp.
        """
        path = self.raw_tsi_mask_path(timestamp)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def validate_csv(self, filename):
        """
        Looks at all of the timestamps in filename (a .csv file) and remembers how many were valid (i.e., have
        non-empty photos and TSI masks. Also ignores duplicate timestamps. This method is not necessary during normal
        processing, but may be helpful for verifying that files exist, counting invalid timestamps, etc.
        """
        path = self.raw_csv_dir + '/' + filename
        print('Validating ' + path)
        data = pd.read_csv(path, converters={'timestamp_utc': str})
        print('Data size before removing duplicates: {}'.format(len(data)))
        data = data.drop_duplicates(subset='timestamp_utc')
        print('Data size after removing duplicates: {}'.format(len(data)))
        timestamps = data['timestamp_utc']
        self.valid_timestamp_count = 0
        self.invalid_timestamp_count = 0
        for i, t in timestamps.items():
            if i % 10000 == 0:
                print(i)
            if self.photo_exists(t) and self.tsi_mask_exists(t):
                self.valid_timestamp_count += 1
            else:
                print(t)
                self.invalid_timestamp_count += 1
        print('Valid timestamps: ' + str(self.valid_timestamp_count))
        print('Invalid timestamps: ' + str(self.invalid_timestamp_count))

    def write_clean_csv(self, filename):
        """
        Writes a cleaned-up version of filename. The filename is read from this Preprocessor's raw_csv_dir and the
        clean version is written to this Preprocessor's data_dir. "Cleaning" means removing duplicate timestamps and
        eliminating timestamps where either the photo or TSI mask is nonexistent or empty.
        """
        in_path = self.raw_csv_dir + '/' + filename
        print('Reading ' + in_path)
        data = pd.read_csv(in_path, converters={'timestamp_utc': str})
        data = data.drop_duplicates(subset='timestamp_utc')
        valid = data['timestamp_utc'].map(lambda t: self.photo_exists(t) and self.tsi_mask_exists(t))
        data = data[valid]
        out_path = self.data_dir + '/' + filename
        print('Writing ' + out_path)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        data.to_csv(out_path, index=False)
        print('Done')


if __name__ == '__main__':
    p = Preprocessor('/home/users/jkleiss/TSI_C1', '../raw_csv', '../data')
    p.write_clean_csv('shcu_dubious_data.csv')
    p.write_clean_csv('shcu_typical_data.csv')
