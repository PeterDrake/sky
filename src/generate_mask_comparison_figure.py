from utils_timestamp import *
from config import *
from skimage.io import imsave, imread
import matplotlib.pyplot as plt


# Display one
def show_mask_comparison_figure(timestamp):
    """Quick utility to display a model's prediction."""
    photo = imread(timestamp_to_photo_path('../test_data', timestamp))
    tsi_mask = imread(timestamp_to_tsi_mask_path('../test_data', timestamp))
    network_mask = imread(timestamp_to_network_mask_path('../results/' + EXPERIMENT_NAME, timestamp))
    fig, ax = plt.subplots(1, 3, figsize=(9, 3))
    fig.suptitle(timestamp)
    ax[0].imshow(photo)
    ax[0].set_title('Photo')
    ax[1].imshow(tsi_mask)
    ax[1].set_title('TSI Mask')
    ax[2].imshow(network_mask)
    ax[2].set_title('Network Mask')


show_mask_comparison_figure('20170524180130')
