#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues, June 26 2017
@author: Maxwell Levin
"""

import matplotlib.pyplot as plt

exp_label = "e72-00"
with open("results/" + exp_label + "/output.txt") as f:
	x, train, valid = [], [], []
	for line in f.readlines()[1:]:
		line = line.split()
		x.append(int(line[0]))
		train.append(float(line[1]))
		valid.append(float(line[2]))
	with plt.xkcd():
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		ax.set_xlabel("Epoch")
		ax.set_ylabel("Accuracy")
		ax.set_title("Accuracy vs. Epoch (Network #2)")
		ax.plot(x, train, label="training")
		ax.plot(x, valid, label="validation")
		ax.legend(loc='lower right')
		plt.tight_layout()
		fig.show()
		fig.savefig('results/accuracy_vs_epoch_' + exp_label + '_.png', dpi=300, bbox_inches='tight')

# print(train)
# print(valid)


# lines = lines[1:]  # Strip off header line
# train = [row.split('\t')[1] for row in lines]
# valid = [row.split('\t')[2] for row in lines]

# data = np.empty((1, 80))
#
# # Read in data
# for i in [11]:
#     with open("results/exp49-" + str(i).rjust(2, '0') + "/output.txt") as f:
#         lines = f.readlines()
#     lines = lines[1:]  # Strip off header line
#     train = [row.split('\t')[1] for row in lines]
#     valid = [row.split('\t')[2] for row in lines]
#
# print(data)
#
# #plt.xkcd()
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_xlabel('Minibatches of 50 training images')
# ax1.set_ylabel('Accuracy')
# x = range(25, 2001, 25)
# t, = ax1.plot(x, train, 'r', label='training')
# v, = ax1.plot(x, valid, 'b', label='validation')
# ax1.legend(bbox_to_anchor=(1, 0.2), handles=[t, v])
# fig.savefig('results/poster_plot.png', dpi=300, bbox_inches='tight')
