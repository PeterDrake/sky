import pandas as pd
from utils_timestamp import *
from dotenv import load_dotenv
import os
import pysftp
from config import *


class GlareRemover:
    """
    Reclassifies (as clear sky) all cloud pixels in images that we think are likely to contain mostly
    sun glare (as defined in has_glare).
    """
    def __init__(self, data_dir, verbose=True):
        self.data_dir = data_dir
        self.verbose = verbose

    def pull_files(self, timestamps):
        load_dotenv()
        user = os.environ.get('user')
        password = os.environ.get('password')
        with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
            for t in timestamps:
                connection.get(f'{DATA_DIR}/photos/{yyyymmdd(t)}/{t}_photo.jpg',
                               f'../data_for_plotting/{t}_photo.jpg')
                connection.get(f'{DATA_DIR}/tsi_masks/{yyyymmdd(t)}/{t}_tsi_mask.png',
                               f'../data_for_plotting/{t}tsi_mask.png')

    def has_glare(self, timestamps, fscs):
        """
        An image is assumed to have glare if:
        a) It has TSI FSC (total thin + opaque) < 0.1, AND
        b) It is before 11 AM or after 5 PM Oklahoma standard time.
        """
        hours = timestamps.map(lambda t: int(hhmmss(t)[:2]))
        # print(hours.value_counts())
        return (fscs < 0.1) & ((hours < 17) | (hours >= 23))

    def find_glare_files(self, csv):
        result = pd.read_csv(csv, converters={'timestamp_utc': str})
        result['total'] = result['clear_100'] + result['thin_100'] + result['opaque_100']
        result['fsc_thin_100'] = result['thin_100'] / result['total']
        result['fsc_opaque_100'] = result['opaque_100'] / result['total']
        result['glare'] = self.has_glare(result['timestamp_utc'], result['fsc_thin_100'] + result['fsc_opaque_100'])
        # print(self.counts)
        print(result['glare'].mean())
        self.pull_files(list(result[result['glare']]['timestamp_utc'])[::100])

    def log(self, message):
        if self.verbose:
            print(message)

    def preprocess_timestamp(self, timestamp):
        # # Read in mask and photo
        # mask = imread(self.raw_tsi_mask_path(timestamp))[:, :, :3]
        # photo = imread(self.raw_photo_path(timestamp))[:, :, :3]
        # # Process them in memory
        # coords = center_and_radius(mask)
        # mask = crop(mask, coords)
        # mask = remove_sun(mask)
        # mask = remove_green_lines(mask)
        # photo = crop(photo, coords)
        # photo = blacken_outer_ring(photo, coords)
        # # Write revised versions
        # imsave(timestamp_to_tsi_mask_path(self.data_dir, timestamp), mask)
        # imsave(timestamp_to_photo_path(self.data_dir, timestamp), photo)
        pass

    def preprocess_images(self, csv_filename):
        # """
        # Preprocesses each image with timestamp in csv_filename (which is in self.data_dir), writing new version of
        # the photo and tsi_mask files into self.data_dir.
        # """
        # csv = self.data_dir + '/' + csv_filename
        # self.log('Reading ' + csv)
        # data = pd.read_csv(csv, converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
        # self.log('Preprocessing ' + str(len(data)) + ' images')
        # for i, t in data['timestamp_utc'].items():
        #     self.preprocess_timestamp(t)
        #     if i % 1000 == 0:
        #         self.log(str(i) + ' images preprocessed')
        # self.log('Done preprocessing images')
        pass

# g = GlareRemover()
# g.find_glare_files('../data_for_plotting/typical_validation_tsi_fsc.csv')
