from skimage.io import imread
import matplotlib.pyplot as plt
from utils_timestamp import *
from config import *
from dotenv import load_dotenv
import os
import pysftp
from ExperimentLogUpdater import ExperimentLogUpdater


def fetch_images_from_blt(timestamp):
    """
    Fetches the photo, TSI mask, and network mask for timestamp from BLT via sftp. The files are saved into
    data_for_plotting.
    """
    load_dotenv()
    user = os.environ.get('user')
    password = os.environ.get('password')
    with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
        connection.get(timestamp_to_photo_path(DATA_DIR, timestamp),
                       '../data_for_plotting/' + timestamp + '_photo.jpg')
        connection.get(timestamp_to_tsi_mask_path(DATA_DIR, timestamp),
                       '../data_for_plotting/' + timestamp + '_tsi_mask.png')
        log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, True)
        print('Looking in ' + timestamp_to_network_mask_path(log_updater.experiment_dir, timestamp))
        connection.get(timestamp_to_network_mask_path(log_updater.experiment_dir, timestamp),
                       '../data_for_plotting/' + timestamp + '_network_mask.png')


# Display one image: photo, tsi_mask, and network_mask.
def show_mask_comparison_figure(timestamp):
    """Quick utility to display a model's prediction."""
    photo = imread('../data_for_plotting/' + timestamp + '_photo.jpg')
    tsi_mask = imread('../data_for_plotting/' + timestamp + '_tsi_mask.png')
    network_mask = imread('../data_for_plotting/' + timestamp + '_network_mask.png')
    fig, ax = plt.subplots(1, 3, figsize=(9, 3))
    fig.suptitle(timestamp)
    ax[0].imshow(photo)
    ax[0].set_title('Photo')
    ax[1].imshow(tsi_mask)
    ax[1].set_title('TSI Mask')
    ax[2].imshow(network_mask)
    ax[2].set_title('Network Mask')
    plt.show()


timestamp = '20160525195830'
fetch_images_from_blt(timestamp)
show_mask_comparison_figure(timestamp)

