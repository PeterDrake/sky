#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ad-hoc script to generate conditions.txt, which describes experimental
conditions for training. Run this before launching the training task.

@author: Peter Drake, Maxwell Levin, Zoe Harrington
"""

exp = 73
i = 0
variants = [
	'a:conv-{0}-{1}-in b:conv-{0}-{2}-a c:conv-{0}-{3}-b d:conv-{0}-{4}-c e:conv-{0}-{5}-d f:concat-e-in g:conv-{'
	'0}-4-f']

with open("conditions.txt", 'w') as conditions:
	for v in variants:
		for j in range(2):
			conditions.write('e{}-{:0>2} '.format(exp, i) + v.format(3, 32, 48, 64, 80, 96) + "\n")
			i += 1

# with open("conditions.txt", 'w') as conditions:
# 	for v in variants:
# 		for kernel_width in [3]:
# 			for channels in [32, 48, 64]:
# 				for j in range(2):
# 					conditions.write('e{}-{:0>2} '.format(exp, i) + v.format(kernel_width, channels) + "\n")
# 					i += 1
