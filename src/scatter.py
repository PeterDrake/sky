import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../plotting_data/collate_fsc_cf_dubious.csv')
df['fsc'] = df['opaque_160'] / (df['clear_160'] + df['thin_160'] + df['opaque_160'])
plt.scatter(df['cf_shcu'], df['fsc'], s=0.1)
# plt.scatter(df['cf_tot'], df['fsc_z'], s=0.1)
plt.title('Dubious data')
plt.xlabel('CF')
plt.ylabel('TSI FSC')
plt.plot([0,1], [0, 1], color='orange')
plt.show()
