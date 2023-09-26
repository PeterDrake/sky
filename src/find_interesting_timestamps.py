import pandas as pd
import random

"""
Finds some representative timestamps for manual inspections.
"""

net = pd.read_csv('../data_for_plotting/collate_network_fsc_cf_typical.csv', dtype={'timestamp_utc':str})
tsi = pd.read_csv('../data_for_plotting/collate_tsi_fsc_cf_typical.csv', dtype={'timestamp_utc':str})
df = net.merge(tsi, how='outer', on=('timestamp_utc', 'cf_shcu'), suffixes=('_net', '_tsi'))
df.set_index('timestamp_utc', inplace=True)
print(df.columns.values)
# print(df.head())
# Make new columns for differences
df['cloud_net'] = df['fsc_thin_100_net'] + df['fsc_opaque_100_net']
df['cloud_tsi'] = df['fsc_thin_100_tsi'] + df['fsc_opaque_100_tsi']
df['tsi-net'] = df['cloud_tsi'] - df['cloud_net']
df['tsi-cf'] = df['cloud_tsi'] - df['cf_shcu']
df['net-cf'] = df['cloud_net'] - df['cf_shcu']
desired_cfs = (0.0, 0.25, 0.5, 0.75, 1.0)
tolerance = 0.01
for desired in desired_cfs:
    print(f'cf: {desired}')
    rows = df[(desired - tolerance < df['cf_shcu']) & (df['cf_shcu'] < desired + tolerance)]
    # i = rows.iloc[rows['tsi-net'].idxmax()]
    print(f'images found: {len(rows)}')
    stamps = (rows['tsi-net'].idxmax(axis=0),
              rows['tsi-net'].idxmin(axis=0),
              rows['tsi-cf'].idxmax(axis=0),
              rows['tsi-cf'].idxmin(axis=0),
              rows['net-cf'].idxmax(axis=0),
              rows['net-cf'].idxmin(axis=0),)
    for stamp in stamps:
        row = rows.loc[stamp]
        print(f'{stamp}  tsi: {row["cloud_tsi"]:.3f}  net: {row["cloud_net"]:.3f}  cf: {row["cf_shcu"]:.3f}')

    # i = rows['tsi-net'].idxmax(axis=0)
    # # print(f'i: {i}')
    # row = rows.loc[i]
    # print(f'{i}  tsi: {row["cloud_tsi"]:.3f}  net: {row["cloud_net"]:.3f}  cf: {row["cf_shcu"]:.3f}')

