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


"""
Downloads (from BLT) various files for the current experiment and then saves into a subdirectory of data_for_plotting:

1. Those files
2. rmse.txt, giving the RMSE values for fsc vs cf
3. stamps.txt, giving some 'interesting' timestamps
4. A triptych for each of these timestamps
5. The scatter plots of fsc vs cf
6. The learning curve
"""


def download_files():
    """
    Fetches the photo, TSI mask, and network mask for timestamp from BLT via sftp. The files are saved into
    data_for_plotting.
    """
    Path(dir).mkdir(exist_ok=True)
    load_dotenv()
    user = os.environ.get('user')
    password = os.environ.get('password')
    with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
        for quality in ('typical', 'dubious'):
            connection.get(f'{DATA_DIR}/collate_tsi_fsc_cf_{quality}.csv',
                           f'{dir}/collate_tsi_fsc_cf_{quality}.csv')
            connection.get(f'{RESULTS_DIR}/{EXPERIMENT_NAME}/collate_network_fsc_cf_{quality}.csv',
                           f'{dir}/collate_network_fsc_cf_{quality}.csv')
        connection.get(f'{RESULTS_DIR}/{EXPERIMENT_NAME}/training_history',
                       f'{dir}/training_history')


def rmse():
    with open(f'{dir}/rmse.txt', 'w') as file:
        for source in ('tsi', 'network'):
            file.write(f'{source}: ')
            for quality in ('typical', 'dubious'):
                df = pd.read_csv(f'{dir}/collate_{source}_fsc_cf_{quality}.csv')
                df.dropna(inplace=True)
                rmse = mean_squared_error(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], squared=False)
                file.write(f'{quality}: {rmse:.3f} ')
            file.write('\n')


def find_interesting_timestamps(quality):
    with open(f'{dir}/{quality}_stamps.txt', 'w') as file:
        net = pd.read_csv(f'{dir}/collate_network_fsc_cf_{quality}.csv', dtype={'timestamp_utc': str})
        tsi = pd.read_csv(f'{dir}/collate_tsi_fsc_cf_{quality}.csv', dtype={'timestamp_utc': str})
        df = net.merge(tsi, how='outer', on=('timestamp_utc', 'cf_shcu'), suffixes=('_net', '_tsi'))
        df.set_index('timestamp_utc', inplace=True)
        # Make new columns for differences
        df['cloud_net'] = df['fsc_thin_100_net'] + df['fsc_opaque_100_net']
        df['cloud_tsi'] = df['fsc_thin_100_tsi'] + df['fsc_opaque_100_tsi']
        df['tsi-net'] = df['cloud_tsi'] - df['cloud_net']
        df['tsi-cf'] = df['cloud_tsi'] - df['cf_shcu']
        df['net-cf'] = df['cloud_net'] - df['cf_shcu']
        desired_cfs = (0.0, 0.25, 0.5, 0.75, 1.0)
        tolerance = 0.01
        result = []
        for desired in desired_cfs:
            file.write(f'cf: {desired}\n')
            rows = df[(desired - tolerance < df['cf_shcu']) & (df['cf_shcu'] < desired + tolerance)]
            file.write(f'images found: {len(rows)}\n')
            stamps = (rows['tsi-net'].idxmax(axis=0),
                      rows['tsi-net'].idxmin(axis=0),
                      rows['tsi-cf'].idxmax(axis=0),
                      rows['tsi-cf'].idxmin(axis=0),
                      rows['net-cf'].idxmax(axis=0),
                      rows['net-cf'].idxmin(axis=0),)
            result += stamps
            for stamp in stamps:
                row = rows.loc[stamp]
                file.write(f'{stamp}  tsi: {row["cloud_tsi"]:.3f}  net: {row["cloud_net"]:.3f}  cf: {row["cf_shcu"]:.3f}\n')
        return result


def fetch_images_from_blt(timestamps):
    """
    Fetches the photo, TSI mask, and network mask for timestamp from BLT via sftp. The files are saved into
    data_for_plotting.
    """
    load_dotenv()
    user = os.environ.get('user')
    password = os.environ.get('password')
    with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
        for s in timestamps:
            connection.get(timestamp_to_photo_path(DATA_DIR, s),
                           f'{dir}/{s}_photo.jpg')
            connection.get(timestamp_to_tsi_mask_path(DATA_DIR, s),
                           f'{dir}/{s}_tsi_mask.png')
            log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, True)
            # print('Looking in ' + timestamp_to_network_mask_path(log_updater.experiment_dir, s))
            connection.get(timestamp_to_network_mask_path(log_updater.experiment_dir, s),
                           f'{dir}/{s}_network_mask.png')


def create_triptych(timestamp):
    """
    Display one image: photo, tsi_mask, and network_mask.
    """
    photo = imread(f'{dir}/{timestamp}_photo.jpg')
    tsi_mask = imread(f'{dir}/{timestamp}_tsi_mask.png')
    network_mask = imread(f'{dir}/{timestamp}_network_mask.png')
    fig, ax = plt.subplots(1, 3, figsize=(9, 3))
    fig.suptitle(timestamp)
    ax[0].imshow(photo)
    ax[0].set_title('Photo')
    ax[1].imshow(tsi_mask)
    ax[1].set_title('TSI Mask')
    ax[2].imshow(network_mask)
    ax[2].set_title('Network Mask')
    plt.savefig(f'{dir}/{timestamp}_triptych.png')
    plt.close()


def create_scatter_plot():
    plt.figure(figsize=(9, 4))
    ax1 = plt.subplot(121)
    df = pd.read_csv(f'{dir}/collate_network_fsc_cf_typical.csv')
    ax1.scatter(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], s=0.5, alpha=0.5)
    ax1.plot([0, 1], [0, 1], color='red')
    ax1.set_xlabel('Cloud fraction')
    ax1.set_ylabel('Network FSC (opaque + thin, 100)')
    ax1.set_title('Typical data')
    ax1.grid()

    ax2 = plt.subplot(122)
    df = pd.read_csv(f'{dir}/collate_network_fsc_cf_dubious.csv')
    ax2.scatter(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], s=0.5, alpha=0.5)
    ax2.plot([0, 1], [0, 1], color='red')
    ax2.set_xlabel('Cloud fraction')
    # ax2.set_ylabel('Network FSC (opaque, 100)')
    ax2.set_title('Dubious data')
    ax2.grid()
    plt.savefig(f'{dir}/scatter.png')
    plt.close()


def create_learning_curve():
    df = pd.read_csv(f'{dir}/training_history')
    df.plot('Epoch', ['loss', 'val_loss'])
    x = list(df['Epoch'])[-1]
    y = list(df['val_loss'])[-1]
    plt.text(x, y * 1.5, f'{y:.3f}', horizontalalignment='center')
    plt.grid()
    plt.savefig(f'{dir}/learning_curve.png')
    plt.close()


# Now, time to call those functions!
dir = f'../data_for_plotting/{EXPERIMENT_NAME}'
download_files()
rmse()
for quality in ('typical', 'dubious'):
    stamps = find_interesting_timestamps(quality)
    fetch_images_from_blt(stamps)
    for i, s in enumerate(stamps):
        print(i)
        create_triptych(s)
create_scatter_plot()
create_learning_curve()
