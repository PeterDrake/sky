#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:11:15 2017

@author: drake
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 09:45:01 2017
@author: drake
"""

import matplotlib.pyplot as plt
import numpy as np

data = np.empty((1, 80))

# Read in data
for i in [11]:
    with open("results/exp49-" + str(i).rjust(2, '0') + "/output.txt") as f:
        lines = f.readlines()
    lines = lines[1:]  # Strip off header line
    train = [row.split('\t')[1] for row in lines]
    valid = [row.split('\t')[2] for row in lines]

print(data)

#plt.xkcd()
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Minibatches of 50 training images')
ax1.set_ylabel('Accuracy')
x = range(25, 2001, 25)
t, = ax1.plot(x, train, 'r', label='training')
v, = ax1.plot(x, valid, 'b', label='validation')
ax1.legend(bbox_to_anchor=(1, 0.2), handles=[t, v])
fig.savefig('results/poster_plot.png', dpi=300, bbox_inches='tight')
