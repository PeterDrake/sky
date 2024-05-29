import pandas as pd
from sklearn.metrics import mean_squared_error
from config import *
from dotenv import load_dotenv
import os
import pysftp
from pathlib import Path
from utils_timestamp import *
from ExperimentLogUpdater import ExperimentLogUpdater
from skimage.io import imread
import matplotlib.pyplot as plt
import math

"""
Downloads (from BLT) a photo, a TSI mask, and network masks for a variety of experiments for a single specified
timestamp. Those files, along with a combined comparison figure, are saved in a subdirectory of data_for_plotting.
"""

def download_files(timestamp, experiment_names):
    """
    Fetches the photo, TSI mask, and network masks (from each specified experiment) for timestamp from BLT via sftp.
    The files are saved into a directory within data_for_plotting.
    """
    dir = f'../data_for_plotting/{timestamp}'
    Path(dir).mkdir(exist_ok=True)
    load_dotenv()
    user = os.environ.get('user')
    password = os.environ.get('password')
    with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
        connection.get(timestamp_to_photo_path(DATA_DIR, timestamp),
                       f'{dir}/{timestamp}_photo.jpg')
        connection.get(timestamp_to_tsi_mask_path(DATA_DIR, timestamp),
                       f'{dir}/{timestamp}_tsi_mask.png')
        for e in experiment_names:
            log_updater = ExperimentLogUpdater(RESULTS_DIR, e)
            print(timestamp_to_network_mask_path(log_updater.experiment_dir, timestamp))
            connection.get(timestamp_to_network_mask_path(log_updater.experiment_dir, timestamp),
                           f'{dir}/{timestamp}_{e}_network_mask.png')


def produce_comparison_figure(timestamp, experiment_names):
    dir = f'../data_for_plotting/{timestamp}'
    photo = imread(f'{dir}/{timestamp}_photo.jpg')
    tsi_mask = imread(f'{dir}/{timestamp}_tsi_mask.png')
    network_masks = [imread(f'{dir}/{timestamp}_{e}_network_mask.png') for e in experiment_names]
    n = len(network_masks) + 2
    rows = int(n ** 0.5)
    cols = math.ceil(n / rows)
    fig, ax = plt.subplots(rows, cols, figsize=(9, 9))
    fig.suptitle(timestamp)
    ax = ax.flatten()
    ax[0].imshow(photo)
    ax[0].set_title('Photo')
    ax[1].imshow(tsi_mask)
    ax[1].set_title('TSI Mask')
    for i, e in enumerate(experiment_names):
        ax[2 + i].imshow(network_masks[i])
        ax[2 + i].set_title(e)
    plt.savefig(f'{dir}/comparison.png')
    plt.show()
    plt.close()


timestamp = '20150831190500'
experiments = ['su24_001_no_glare',
               'su24_002_no_glare',
               'su24_003_no_glare',
               'su24_004_no_glare',
               'su24_007_no_glare',
               'su24_008_no_glare']
download_files(timestamp, experiments)
produce_comparison_figure(timestamp, experiments)
