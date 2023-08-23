import pandas as pd
import random

"""
Finds some representative timestamps for manual inspections.
"""

df = pd.read_csv('../data_for_plotting/collate_network_fsc_cf_dubious.csv')
desired_cfs = (0.0, 0.25, 0.5, 0.75, 1.0)
tolerance = 0.001
for desired in desired_cfs:
    print(desired)
    rows = df[(desired - tolerance < df['cf_shcu']) & (df['cf_shcu'] < desired + tolerance)]
    print(rows.sample(n=1))
