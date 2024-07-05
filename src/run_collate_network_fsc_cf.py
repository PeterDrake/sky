import pandas as pd
from config import *

def collate_network_fsc_cf(quality, category):
    '''
    :param quality either 'typical' or 'dubious'
    :param category either 'validation' or 'testing'
    '''
    # Read the network FSCs
    network_fsc_df = pd.read_csv(f'{RESULTS_DIR}/{EXPERIMENT_NAME}/{quality}_{category}_network_fsc_20avg.csv')
    # Read the ceilometer CFs
    cf_df = pd.read_csv(RAW_CSV_DIR + '/shcu_' + quality + '_data.csv', usecols=['timestamp_utc', 'cf_shcu'])
    cf_df = cf_df.drop_duplicates()
    # Join the dataframes
    result = network_fsc_df.merge(cf_df, on='timestamp_utc', how='inner')
    # Export the result
    result.to_csv(RESULTS_DIR + '/' + EXPERIMENT_NAME + '/collate_network_fsc_cf_' + quality + '.csv')

collate_network_fsc_cf('typical', 'testing')
collate_network_fsc_cf('dubious', 'testing')
