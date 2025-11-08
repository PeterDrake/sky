import pandas as pd
import matplotlib.pyplot as plt

plt.figure(figsize=(9, 4))

ax1 = plt.subplot(121)
df = pd.read_csv('../data_for_plotting/collate_network_fsc_cf_typical.csv')
ax1.scatter(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], s=0.5, alpha=0.5)
ax1.plot([0, 1], [0, 1], color='red')
ax1.set_xlabel('Cloud fraction')
ax1.set_ylabel('Network FSC (opaque + thin, 100)')
ax1.set_title('Typical data')
ax1.grid()

ax2 = plt.subplot(122)
df = pd.read_csv('../data_for_plotting/collate_network_fsc_cf_dubious.csv')
ax2.scatter(df['cf_shcu'], df['fsc_opaque_100'] + df['fsc_thin_100'], s=0.5, alpha=0.5)
ax2.plot([0, 1], [0, 1], color='red')
ax2.set_xlabel('Cloud fraction')
# ax2.set_ylabel('Network FSC (opaque, 100)')
ax2.set_title('Dubious data')
ax2.grid()

plt.show()
