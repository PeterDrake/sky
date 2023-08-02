import pandas as pd
import matplotlib.pyplot as plt

# plt.figure(figsize=(9, 4))

df = pd.read_csv('../data_for_plotting/training_history')
df.plot('Epoch', ['loss', 'val_loss'])

x = list(df['Epoch'])[-1]
y = list(df['val_loss'])[-1]
plt.text(x, y * 1.5, f'{y:.3f}', horizontalalignment='center')

plt.grid()

plt.show()