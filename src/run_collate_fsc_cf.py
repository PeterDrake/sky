import pandas as pd
from config import *

# Read the timestamps
with open(DATA_DIR + '/' + TYPICAL_TIMESTAMP_FILENAMES[1], 'r') as f:
    val_stamps = [line.strip() for line in f.readlines()]

# Read the TSI FSCs
tsi_fsc_df = pd.read_csv(DATA_DIR + '/typical_validation_tsi_fsc.csv', index_col=0)
tsi_fsc_df.index.name = 'timestamp_utc'
print(tsi_fsc_df.info())

# Read the ceilometer CFs
cf_df = pd.read_csv(RAW_CSV_DIR + '/shcu_typical_data.csv', usecols=['timestamp_utc', 'cf_shcu'])
print(cf_df.info())

# Join the dataframes
result = tsi_fsc_df.merge(cf_df, on='timestamp_utc', how='inner')
print(result.info())

# Export the result
result.to_csv(RESULTS_DIR + '/' + EXPERIMENT_NAME + '/' + 'collate_fsc_cf.csv')
