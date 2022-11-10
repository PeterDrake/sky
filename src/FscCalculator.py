from utils_image import *
import pandas as pd
from utils_timestamp import *
import os
from skimage.io import imread


class FscCalculator:

    def __init__(self, timestamp_dir, mask_dir, output_dir):
        self.timestamp_dir = timestamp_dir
        self.mask_dir = mask_dir
        self.output_dir = output_dir

    def count_pixels(self, mask):
        """
        Returns the number of blue, gray and white pixels in mask.
        :param mask: 480x480x3 numpy array
        """
        return [(mask == c).all(axis=2).sum() for c in [BLUE, GRAY, WHITE]]

    def timestamp_to_mask_path(self, timestamp):
        """
        Returns the full path for the network or TSI mask file for the given timestamp.
        Note that self.mask_dir indicates if we desire a tsi or network mask. Use this information to obtain
        the correct filename ('*_network_* or *_tsi_*).
        """
        if 'network_masks' in self.mask_dir:
            suffix = '_network_mask.png'
        else:
            suffix = '_tsi_mask.png'
        mask_path = self.mask_dir + '/' + yyyymmdd(timestamp) + '/' + timestamp + suffix
        if os.path.exists(mask_path):
            return mask_path
        else:
            print('Could not find ' + mask_path)
            exit()

    def count_pixels_in_all_masks(self, stamps):
        """
        Return a dataframe containing the clear/thin/opaque counts for all masks in the list of stamps.
        """
        # TODO The index should be named something like timestamp
        result = pd.DataFrame(index=stamps, columns=('clear_160', 'thin_160', 'opaque_160'))
        for timestamp in stamps:
            mask = imread(self.timestamp_to_mask_path(timestamp))[:, :, :3]
            counts_160 = self.count_pixels(mask) # in the full mask
            result.loc[timestamp] = counts_160
        return result

    def write_pixel_counts(self, timestamp_filename, output_filename):
        with open(self.timestamp_dir + '/' + timestamp_filename, 'r') as f:
            stamps = [line.strip() for line in f.readlines()]
        df = self.count_pixels_in_all_masks(stamps)
        df.to_csv(self.output_dir + '/' + output_filename)
