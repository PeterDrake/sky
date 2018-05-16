#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plots a learning curve showing the network's performance on training and
validation sets over the course of training.

Command line arguments:
dir

dir is the results directory where the network is stored.

Created on Fri Jun  9 09:30:05 2017

@author: drake
"""

import matplotlib.pyplot as plt
import sys

file = dir_name = "results/" + sys.argv[1] + "/output.txt"

with open(file) as f:
    data = f.readlines()

data = data[1:]  # Strip off first and last line
x = [row.split('\t')[0] for row in data]
train = [row.split('\t')[1] for row in data]
valid = [row.split('\t')[2] for row in data]

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Minibatches')
ax1.set_ylabel('Accuracy')
t, = ax1.plot(x, train, 'r', label='training')
v, = ax1.plot(x, valid, 'b', label='validation')
ax1.legend(handles=[t, v])
plt.show()
