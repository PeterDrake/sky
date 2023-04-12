import pandas as pd
import matplotlib.pyplot as plt

network = pd.read_csv('../data_for_plotting/typical_validation_network_fsc.csv', index_col=0)
tsi = pd.read_csv('../data_for_plotting/typical_validation_tsi_fsc.csv', index_col=0)
tsi.index.name = 'timestamp_utc'

cf = pd.read_csv('../raw_csv/shcu_typical_data.csv', usecols=['timestamp_utc', 'cf_shcu'])
cf = cf.set_index('timestamp_utc')
print(tsi.info())
cf_merged = tsi.merge(cf, how='inner', left_index=True, right_index=True)
print(cf_merged.info())
# print(cf_merged[:10])
# print(tsi[:10])

def pixels_to_fsc(f):
    """
    Given a dataframe f with counts of each type of pixel, return a sequence of FSC values.
    """
    return (f['opaque_160'] + f['thin_160']) / (f['opaque_160'] + f['thin_160'] + f['clear_160'])


network_fsc = pixels_to_fsc(network)
tsi_fsc = pixels_to_fsc(tsi)

plt.scatter(tsi_fsc, network_fsc, s=0.5, alpha=0.5)
plt.plot([0, 1], [0, 1], color='red')
plt.xlabel('tsi')
plt.ylabel('network')
plt.grid()
plt.show()
