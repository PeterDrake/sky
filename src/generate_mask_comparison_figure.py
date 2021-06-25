from utils_timestamp import *
from config import *
from skimage.io import imsave, imread
import matplotlib.pyplot as plt
import glob
import os

# Set directories here for visualizations. (No need to edit our config file!)
real_dirs = {'raw_data_dir':'../raw_data',
        'raw_csv_dir':'../raw_csv',
        'data_dir':'../data',
        'results_dir':'../results'}

# Note - if you want to run these on the test data, use the following:
test_dirs = {'raw_data_dir':'../test_raw_data',
             'raw_csv_dir':'../test_raw_csv',
             'data_dir':'../test_data',
             'results_dir':'../results'}

# Display one image: photo, tsi_mask, and network_mask.
# Note: use the TEST directories for show_mask_comparison_figure, for now.  JMK June 25, 2021.
def show_mask_comparison_figure(timestamp, dirs):
    """Quick utility to display a model's prediction."""
    photo = imread(timestamp_to_photo_path(dirs['data_dir'], timestamp))
    tsi_mask = imread(timestamp_to_tsi_mask_path(dirs['data_dir'], timestamp))
    network_mask = imread(timestamp_to_network_mask_path(dirs['results_dir'] + '/' + EXPERIMENT_NAME, timestamp))
    fig, ax = plt.subplots(1, 3, figsize=(9, 3))
    fig.suptitle(timestamp)
    ax[0].imshow(photo)
    ax[0].set_title('Photo')
    ax[1].imshow(tsi_mask)
    ax[1].set_title('TSI Mask')
    ax[2].imshow(network_mask)
    ax[2].set_title('Network Mask')

# I stole this from Preprocessor.py:
def raw_photo_path(timestamp, dirs):
    """Returns the path of a raw photo file, or None if there is no such file."""
    print(dirs)
    result = dirs['raw_data_dir'] + '/SkyImage/'
    allims = glob.glob(result + 'sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '*')
    if not allims:
        return None
    return allims[0] + '/sgptsiskyimageC1.a1.' + yyyymmdd(timestamp) + '.' + hhmmss(timestamp) + '.jpg.' + timestamp + '.jpg'


# I also stole this from Preprocessor.py:
def raw_tsi_mask_path(timestamp, dirs):
    """Returns the path of a raw TSI mask file, or None if there is no such file."""
    result = dirs['raw_data_dir'] + '/CloudMask/'
    allims = result + 'sgptsicldmaskC1.a1.' + yyyymmdd(timestamp)
    if not os.path.exists(allims):
        return None
    return allims + '/sgptsicldmaskC1.a1.' + yyyymmdd(timestamp) + '.' + hhmmss(timestamp) + '.png.' + timestamp + '.png'

# Display the results of preprocessing: Original photo, cropped photo & cropped mask.
def show_preprocessed_images(timestamp, dirs):
    """
    Quick utility to display an original image and the preprocessed image & tsi_mask.
    :param timestamp: The image of interest [yyyymmddHHMMSS]
    :param imdir: The directory of the preprocessed images (typically '../data' or '../test_data'
    """
    skyimage = imread(raw_photo_path(timestamp, dirs))
    print(skyimage.shape)
    cloudmask = imread(raw_tsi_mask_path(timestamp, dirs))
    photo = imread(timestamp_to_photo_path(dirs['data_dir'], timestamp))
    tsi_mask = imread(timestamp_to_tsi_mask_path(dirs['data_dir'], timestamp))
    fig, ax = plt.subplots(2, 2, figsize=(6, 6))
    fig.suptitle(timestamp)
    ax[0,0].imshow(skyimage)
    ax[0,0].set_title('Original Image')
    ax[1, 0].imshow(cloudmask)
    ax[1, 0].set_title('Original Mask')
    ax[0,1].imshow(photo)
    ax[0,1].set_title('Photo')
    ax[1,1].imshow(tsi_mask)
    ax[1,1].set_title('TSI Mask')


# show_mask_comparison_figure('20170524180130', test_dirs)

# show_preprocessed_images('20170918223000', real_dirs)
show_preprocessed_images('20170918224500', real_dirs)