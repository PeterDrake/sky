import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../plotting_data/collate_fsc_cf_typical.csv')
df['fsc'] = df['opaque_100'] / (df['clear_100'] + df['thin_100'] + df['opaque_100'])
plt.scatter(df['cf_shcu'], df['fsc'], s=0.1)
# plt.scatter(df['cf_tot'], df['fsc_z'], s=0.1)
plt.title('Typical data')
plt.xlabel('CF')
plt.ylabel('TSI FSC')
plt.plot([0,1], [0, 1], color='orange')
plt.show()
