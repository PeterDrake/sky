import pandas as pd
from config import *
import sys

suffix = sys.argv[1]

def collate_tsi_fsc_cf(category):
    '''
    :param category either 'typical' or 'dubious'
    '''
    # Read the TSI FSCs
    tsi_fsc_df = pd.read_csv(DATA_DIR + '/' + category + f'_validation_tsi_fsc_20avg{suffix}.csv')
    # Read the ceilometer CFs
    cf_df = pd.read_csv(RAW_CSV_DIR + '/shcu_' + category + '_data.csv', usecols=['timestamp_utc', 'cf_shcu'])
    cf_df = cf_df.drop_duplicates()
    # Join the dataframes
    result = tsi_fsc_df.merge(cf_df, on='timestamp_utc', how='inner')
    # Export the result
    result.to_csv(DATA_DIR + f'{DATA_DIR}/collate_tsi_fsc_cf_{category}{suffix}.csv')

collate_tsi_fsc_cf('typical')
if suffix == '':  # Temporary, because we haven't de-glared dubious data yet
    collate_tsi_fsc_cf('dubious')
