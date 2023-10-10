import pandas as pd
from sklearn.metrics import mean_squared_error
from config import *
from dotenv import load_dotenv
import os
import pysftp
from pathlib import Path

"""
Downloads (from BLT) various files for the current experiment and then saves into a subdirectory of data_for_plotting:

1. Those files
2. rmse.txt, giving the RMSE values for fsc vs cf
3. stamps.txt, giving some 'interesting' timestamps
4. A triptych for each of these timestamps
5. The scattor plots of fsc vs cf
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


def find_interesting_timestamps():
    with open(f'{dir}/stamps.txt', 'w') as file:
        net = pd.read_csv(f'{dir}/collate_network_fsc_cf_typical.csv', dtype={'timestamp_utc': str})
        tsi = pd.read_csv(f'{dir}/collate_tsi_fsc_cf_typical.csv', dtype={'timestamp_utc': str})
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
            for stamp in stamps:
                row = rows.loc[stamp]
                file.write(f'{stamp}  tsi: {row["cloud_tsi"]:.3f}  net: {row["cloud_net"]:.3f}  cf: {row["cf_shcu"]:.3f}\n')


# Now, time to call those functions!
dir = f'../data_for_plotting/{EXPERIMENT_NAME}'
# download_files()
rmse()
find_interesting_timestamps()
