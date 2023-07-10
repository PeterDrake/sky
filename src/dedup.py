import pandas as pd

# Temporary program to check for duplicates in a csv file

df = pd.read_csv('../plotting_data/collate_fsc_cf.csv', index_col=0)
ls = list(df['timestamp_utc'])
print(len(ls))
print(len(set(ls)))

print(df.info())
