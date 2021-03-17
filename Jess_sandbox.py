import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# im = np.array([[0, 1, 0],[1, 1, 0],[2, 1, 0]])
# my_cmap = np.array([(0, 0, 0), (0, 0, 1),(1, 1, 1)],dtype=np.float64)*255

x = np.arange(0, np.pi, 0.1)
y = np.arange(0, 2 * np.pi, 0.1)
X, Y = np.meshgrid(x, y)
Z = np.cos(X) * np.sin(Y) * 10

colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # R -> G -> B
n_bin = 3
cmap_name = 'my_list'
fig, ax = plt.subplots(1,1, figsize=(3,4))
# fig.subplots_adjust(left=0.02, bottom=0.06, right=0.95, top=0.94, wspace=0.05)
# Create the colormap
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
# Fewer bins will result in "coarser" colomap interpolation
im = ax.imshow(Z, origin='lower', cmap=cm)
ax.set_title("N bins: %s" % n_bin)
fig.colorbar(im, ax=ax)