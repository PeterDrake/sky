import pandas as pd
from sklearn.metrics import mean_squared_error

df = pd.read_csv('../data_for_plotting/collate_network_fsc_cf_dubious.csv')
rmse = mean_squared_error(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], squared=False)
print(rmse)
