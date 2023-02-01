import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../plotting_data/collate_fsc_cf.csv')
df['fsc'] = df['opaque_160'] / (df['clear_160'] + df['thin_160'] + df['opaque_160'])
plt.scatter(df['fsc'], df['cf_shcu'], s=0.1)
plt.plot([0,1], [0, 1])
plt.show()
