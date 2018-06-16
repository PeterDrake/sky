#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ad-hoc script to generate conditions.txt, which describes experimental
conditions.

Created on Wed Jul 19 10:04:42 2017

@author: drake
"""

exp = 66
i = 0
variants = ('a:conv-{0}-{1}-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-{0}-{1}-e g:conv-{0}-{1}-f h:concat-g-in i:conv-{0}-4-h',)

with open("conditions.txt", 'w') as conditions:
    for v in variants:
        for kernel_width in (3,):
            for channels in (32,):
                for j in range(5):
                    conditions.write('e{}-{:0>2} '.format(exp, i) + v.format(kernel_width, channels) + "\n")
                    i += 1
