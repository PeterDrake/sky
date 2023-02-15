import pandas as pd
from config import *

def collate_fsc_cf(category):
    '''
    :param category either 'typical' or 'dubious'
    '''
    # Read the TSI FSCs
    tsi_fsc_df = pd.read_csv(DATA_DIR + '/' + category + '_validation_tsi_fsc.csv')
    # tsi_fsc_df.index.name = 'timestamp_utc'
    print(tsi_fsc_df.info())
    # Read the ceilometer CFs
    cf_df = pd.read_csv(RAW_CSV_DIR + '/shcu_' + category + '_data.csv', usecols=['timestamp_utc', 'cf_shcu'])
    print(cf_df.info())
    cf_df = cf_df.drop_duplicates()
    print(cf_df.info())
    # Join the dataframes
    result = tsi_fsc_df.merge(cf_df, on='timestamp_utc', how='inner')
    print(result.info())
    # Export the result
    result.to_csv(RESULTS_DIR + '/' + EXPERIMENT_NAME + '/' + 'collate_fsc_cf_' + category + '.csv')

collate_fsc_cf('typical')
collate_fsc_cf('dubious')