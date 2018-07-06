#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues, June 26 2017
@author: Maxwell Levin
"""

import matplotlib.pyplot as plt

exp_label = "e70-00"
# exp_label = "e72-00"
with open("results/" + exp_label + "/output.txt") as f:
	x, train, valid = [], [], []
	for line in f.readlines()[1:]:
		line = line.split()
		x.append(50 * int(line[0]))
		train.append(float(line[1]))
		valid.append(float(line[2]))
	with plt.xkcd():
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		ax.set_xlabel("Number of Photos Trained On")
		ax.set_ylabel("Accuracy")
		ax.set_title("Machine Learning Curve")
		# ax.set_title("Accuracy vs. Epoch (Network #2)")
		ax.plot(x, train, label="training")
		# ax.plot(x, valid, label="validation")
		# ax.legend(loc='lower right')
		plt.tight_layout()
		# fig.show()
		fig.savefig('results/' + exp_label + '/accuracy_vs_batch_' + exp_label + '.png', dpi=300, bbox_inches='tight')
