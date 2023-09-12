import pandas as pd
from sklearn.metrics import mean_squared_error

for source in ('tsi', 'network'):
    print(source)
    for quality in ('typical', 'dubious'):
        print(quality)
        df = pd.read_csv(f'../data_for_plotting/collate_{source}_fsc_cf_{quality}.csv')
        df.dropna(inplace=True)
        rmse = mean_squared_error(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], squared=False)
        print(rmse)
