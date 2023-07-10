from utils_timestamp import *
from config import *
from skimage.io import imsave, imread
import matplotlib.pyplot as plt
import glob
import os
from Preprocessor import Preprocessor

# Set directories here for visualizations. (No need to edit our config file!)
real_dirs = {'raw_data_dir': '../raw_data',
             'raw_csv_dir': '../raw_csv',
             'data_dir': '../data',
             'experiment_dir': '../results',
             'network_mask_dir': '../results/' + EXPERIMENT_NAME + '/network_masks'}

# Note - if you want to run these on the test data, use the following:
test_dirs = {'raw_data_dir': '../test_raw_data',
             'raw_csv_dir': '../test_raw_csv',
             'data_dir': '../test_data',
             'experiment_dir': '../test_results',
             'network_mask_dir': '../test_network_masks'}


# Display one image: photo, tsi_mask, and network_mask.
# Note: since we don't yet have real data, use dirs=test_dirs for now.  JMK June 25, 2021.
def show_mask_comparison_figure(timestamp, dirs):
    """Quick utility to display a model's prediction."""
    photo = imread(timestamp_to_photo_path(dirs['data_dir'], timestamp))
    tsi_mask = imread(timestamp_to_tsi_mask_path(dirs['data_dir'], timestamp))
    network_mask = imread(timestamp_to_network_mask_path(dirs['network_mask_dir'], timestamp))
    fig, ax = plt.subplots(1, 3, figsize=(9, 3))
    fig.suptitle(timestamp)
    ax[0].imshow(photo)
    ax[0].set_title('Photo')
    ax[1].imshow(tsi_mask)
    ax[1].set_title('TSI Mask')
    ax[2].imshow(network_mask)
    ax[2].set_title('Network Mask')
    plt.show()


# Display the results of preprocessing: Original photo, cropped photo & cropped mask.
def show_preprocessed_images(timestamp, dirs):
    """
    Quick utility to display an original image and the preprocessed image & tsi_mask.
    :param timestamp: The timestamp of the image of interest [yyyymmddHHMMSS]
    :param dirs: A dictionary associating both 'raw_data_dir' and 'data_dir' with directories
    """
    preprocessor = Preprocessor(dirs['raw_data_dir'], None, None)
    skyimage = imread(preprocessor.raw_photo_path(timestamp))
    print(skyimage.shape)
    cloudmask = imread(preprocessor.raw_tsi_mask_path(timestamp))
    photo = imread(timestamp_to_photo_path(dirs['data_dir'], timestamp))
    tsi_mask = imread(timestamp_to_tsi_mask_path(dirs['data_dir'], timestamp))
    fig, ax = plt.subplots(2, 2, figsize=(6, 6))
    fig.suptitle(timestamp)
    fig.subplots_adjust(hspace=0.3)
    ax[0, 0].imshow(skyimage)
    ax[0, 0].set_title('Original Image')
    ax[1, 0].imshow(cloudmask)
    ax[1, 0].set_title('Original Mask')
    ax[0, 1].imshow(photo)
    ax[0, 1].set_title('Photo')
    ax[1, 1].imshow(tsi_mask)
    ax[1, 1].set_title('TSI Mask')
    plt.show()

show_mask_comparison_figure('20120713000000', test_dirs)
# show_mask_comparison_figure('20170524180130', test_dirs)

#show_preprocessed_images('20170524180130', test_dirs)
# show_preprocessed_images('20170918223000', real_dirs)
# show_preprocessed_images('20170918224500', real_dirs)
