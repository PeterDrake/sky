import pandas as pd
from config import *
import sys

def collate_tsi_fsc_cf(quality, category):
    '''
    :param category either 'typical' or 'dubious'
    '''
    # Read the TSI FSCs
    print(f'Collating {quality} {categor}')
    tsi_fsc_df = pd.read_csv(DATA_DIR + '/' + quality + f'_{category}_tsi_fsc_20avg.csv')
    # Read the ceilometer CFs
    cf_df = pd.read_csv(RAW_CSV_DIR + '/shcu_' + quality + '_data.csv', usecols=['timestamp_utc', 'cf_shcu'])
    cf_df = cf_df.drop_duplicates()
    # Join the dataframes
    result = tsi_fsc_df.merge(cf_df, on='timestamp_utc', how='inner')
    # Export the result
    result.to_csv(f'{DATA_DIR}/collate_tsi_fsc_cf_{quality}_{category}.csv')

for quality in ['typical', 'dubious']:
    for category in ['validation', 'testing']:
        collate_tsi_fsc_cf(quality, category)
