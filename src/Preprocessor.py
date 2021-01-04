import glob
import os
import pandas as pd
from utils_timestamp import *


class Preprocessor:

    def __init__(self, raw_data_dir, raw_csv_dir, data_dir, verbose=True):
        self.raw_data_dir = raw_data_dir
        self.raw_csv_dir = raw_csv_dir
        self.data_dir = data_dir
        self.valid_timestamp_count = 'Only meaningful if validate_csv has been called'
        self.invalid_timestamp_count = 'Only meaningful if validate_csv has been called'
        self.verbose = verbose

    def log(self, message):
        if self.verbose:
            print(message)
            
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
        self.log('Validating ' + path)
        data = pd.read_csv(path, converters={'timestamp_utc': str})
        self.log('Data size before removing duplicates: {}'.format(len(data)))
        data = data.drop_duplicates(subset='timestamp_utc')
        self.log('Data size after removing duplicates: {}'.format(len(data)))
        timestamps = data['timestamp_utc']
        self.valid_timestamp_count = 0
        self.invalid_timestamp_count = 0
        for i, t in timestamps.items():
            if i % 10000 == 0:
                self.log(i)
            if self.photo_exists(t) and self.tsi_mask_exists(t):
                self.valid_timestamp_count += 1
            else:
                self.log(t)
                self.invalid_timestamp_count += 1
        self.log('Valid timestamps: ' + str(self.valid_timestamp_count))
        self.log('Invalid timestamps: ' + str(self.invalid_timestamp_count))

    def write_clean_csv(self, filename):
        """
        Writes a cleaned-up version of filename. The filename is read from this Preprocessor's raw_csv_dir and the
        clean version is written to this Preprocessor's data_dir. "Cleaning" means removing duplicate timestamps and
        eliminating timestamps where either the photo or TSI mask is nonexistent or empty.

        This method gets the job done quietly. To instead self.log more information about what's valid, call
        validate_csv instead.
        """
        in_path = self.raw_csv_dir + '/' + filename
        self.log('Reading ' + in_path)
        data = pd.read_csv(in_path, converters={'timestamp_utc': str})
        data = data.drop_duplicates(subset='timestamp_utc')
        valid = data['timestamp_utc'].map(lambda t: self.photo_exists(t) and self.tsi_mask_exists(t))
        data = data[valid]
        out_path = self.data_dir + '/' + filename
        self.log('Writing ' + out_path)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        data.to_csv(out_path, index=False)
        self.log('Done')

    def create_image_directories(self, filename):
        """
        Creates directories within self.data_dir for each unique yyyymmdd date within filename. Filename is a cleaned
        .csv file within self.data_dir. The created directories are photos/yyyymmdd and tsi_masks/yyyymmdd.
        """
        csv = self.data_dir + '/' + filename
        self.log('Reading ' + csv)
        data = pd.read_csv(csv, converters={'timestamp_utc': str})
        timestamps = {yyyymmdd(t) for t in data['timestamp_utc']}
        for prefix in [self.data_dir + '/photos', self.data_dir + '/tsi_masks']:
            if not os.path.exists(prefix):
                os.mkdir(prefix)
            for t in timestamps:
                d = prefix + '/' + t
                if not os.path.exists(d):
                    os.mkdir(d)


if __name__ == '__main__':
    p = Preprocessor('/home/users/jkleiss/TSI_C1', '../raw_csv', '../data')
    p.write_clean_csv('shcu_dubious_data.csv')
    p.write_clean_csv('shcu_typical_data.csv')
