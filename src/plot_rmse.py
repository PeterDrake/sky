import pandas as pd
from sklearn.metrics import mean_squared_error
from config import *
from dotenv import load_dotenv
import os
import pysftp


def fetch_csvs():
    """
    Fetches the photo, TSI mask, and network mask for timestamp from BLT via sftp. The files are saved into
    data_for_plotting.
    """
    load_dotenv()
    user = os.environ.get('user')
    password = os.environ.get('password')
    with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
        for quality in ('typical', 'dubious'):
            connection.get(f'{DATA_DIR}/collate_tsi_fsc_cf_{quality}.csv',
                           f'../data_for_plotting/collate_tsi_fsc_cf_{quality}.csv')
            connection.get(f'{RESULTS_DIR}/{EXPERIMENT_NAME}/collate_network_fsc_cf_{quality}.csv',
                           f'../data_for_plotting/collate_network_fsc_cf_{quality}.csv')


fetch_csvs()
for source in ('tsi', 'network'):
    print(f'{source}: ', end='')
    for quality in ('typical', 'dubious'):
        df = pd.read_csv(f'../data_for_plotting/collate_{source}_fsc_cf_{quality}.csv')
        df.dropna(inplace=True)
        rmse = mean_squared_error(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], squared=False)
        print(f'{quality}: {rmse:.3f} ', end='')
    print()
