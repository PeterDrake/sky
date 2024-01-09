import shutil
import pandas as pd
from utils_timestamp import *
import os
from skimage.io import imsave, imread
from utils_image import remove_all_clouds


class GlareRemover:
    """
    Reclassifies (as clear sky) all cloud pixels in images that we think are likely to contain mostly
    sun glare (as defined in has_glare).
    """
    def __init__(self, data_dir, csv_dir, verbose=True):
        self.data_dir = data_dir  # Where deglared files will be written
        self.csv_dir = csv_dir  # Where the FSC CSV file lives -- the same as data_dir on BLT, different in tests
        self.verbose = verbose

    def has_glare(self, timestamps, fscs):
        """
        An image is assumed to have glare if:
        a) It has TSI FSC (total thin + opaque) < 0.1, AND
        b) It is before 11 AM or after 5 PM Oklahoma standard time.
        """
        hours = timestamps.map(lambda t: int(hhmmss(t)[:2]))
        return (fscs < 0.1) & ((hours < 17) | (hours >= 23))

    def find_glare_files(self, csv):
        result = pd.read_csv(csv, converters={'timestamp_utc': str})
        result['total'] = result['clear_100'] + result['thin_100'] + result['opaque_100']
        result['fsc_thin_100'] = result['thin_100'] / result['total']
        result['fsc_opaque_100'] = result['opaque_100'] / result['total']
        result['glare'] = self.has_glare(result['timestamp_utc'], result['fsc_thin_100'] + result['fsc_opaque_100'])
        return result[result['glare']]['timestamp_utc'], result[~result['glare']]['timestamp_utc']

    def log(self, message):
        if self.verbose:
            print(message)

    def preprocess_timestamp(self, timestamp):
        # Read in mask and photo
        mask = imread(timestamp_to_tsi_mask_path(self.data_dir, timestamp))[:, :, :3]
        # Process them in memory
        mask = remove_all_clouds(mask)
        # Write revised versions
        imsave(timestamp_to_tsi_mask_no_glare_path(self.data_dir, timestamp), mask, check_contrast=False)

    def create_image_directories(self, csv_filename):
        """
        Creates directories within self.data_dir for each unique yyyymmdd date within csv_filename. csv_filename is a
        cleaned .csv file within self.data_dir. The created directories are tsi_masks_no_glare/yyyymmdd.
        """
        csv = self.csv_dir + '/' + csv_filename
        self.log('Reading ' + csv)
        data = pd.read_csv(csv, converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
        self.log('Creating image directories')
        days = {yyyymmdd(t) for t in data['timestamp_utc']}
        for day in days:
            os.makedirs(self.data_dir + '/tsi_masks_no_glare/' + day, exist_ok=True)
        self.log('Done creating image directories')

    def write_deglared_files(self, csv_filename):
        """
        Reads each TSI mask for a timestamp in csv_filename (which is in self.data_dir). Writes either a copy of the
        TSI mask or (if glare is likely) a version with all clouds removed into the tsi_mask_no_glare subdirectory of
        self.data_dir.
        """
        csv = self.csv_dir + '/' + csv_filename
        self.log("Finding glare files")
        glare, no_glare = self.find_glare_files(csv)
        self.log(f'{len(glare)} masks with glare')
        self.log(f'{len(no_glare)} masks without glare')
        # Copy non-problematic files into no_glare directory
        for t in no_glare:
            # os.makedirs(os.path.dirname(timestamp_to_tsi_mask_no_glare_path(self.data_dir, t)), exist_ok=True)
            shutil.copyfile(timestamp_to_tsi_mask_path(self.data_dir, t),
                            timestamp_to_tsi_mask_no_glare_path(self.data_dir, t))
        # Process problematic files and write them into no_glare directory
        for t in glare:
            # os.makedirs(os.path.dirname(timestamp_to_tsi_mask_no_glare_path(self.data_dir, t)), exist_ok=True)
            self.preprocess_timestamp(t)
        self.log('Done removing glare')
        pass
