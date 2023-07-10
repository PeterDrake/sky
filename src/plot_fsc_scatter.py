import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('../data_for_plotting/collate_tsi_fsc_cf_dubious.csv')
df = pd.read_csv('../data_for_plotting/collate_network_fsc_cf_dubious.csv')

plt.scatter(df['fsc_opaque_100'], df['cf_shcu'], s=0.5, alpha=0.5)
plt.plot([0, 1], [0, 1], color='red')
plt.xlabel('TSI fsc (opaque, 100)')
plt.ylabel('Cloud fraction')
plt.grid()
plt.show()
