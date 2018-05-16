#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Displays the kernels in the first hidden layer of the network.

Command line arguments:
dir

dir is the results directory where the network is stored.

Created on Tue Jun 20 11:03:58 2017

@author: jeffmullins
"""
from train import build_net
from show_output import read_parameters, read_last_iteration_number
import numpy as np
import tensorflow as tf
import math
import sys
from PIL import Image

def display_kernels_on_grid (weights, width, num_kernels):
    """Displays kernels on a grid."""
    weights = np.array(weights)
    kernels = np.zeros((num_kernels, width, width, 3))
    for i in range(width):
        for j in range(width):
            for c in range(3): # Color channel
                for r in range(num_kernels):
                    kernels[r][i][j][c] = weights[i][j][c][r]
    # Scale all values to be between 0 and 255
    for i in range(len(kernels)):
        kernels[i] = kernels[i] - np.amin(kernels[i]) 
        kernels[i] = (255 / np.amax(kernels[i])) * kernels[i]
    # Put all kernels onto one image with a layer of black between each
    big_img = np.zeros((math.ceil(num_kernels / 8) * (width + 1) + 1,
                        (width + 1) * 8 + 1, 3))
    for i in range(num_kernels):
        y = (i // 8) * (width + 1) + 1
        x = (i % 8) * (width + 1) + 1
        for r in range(width):
            for c in range(width):
                big_img[r + y][c + x] = kernels[i][r][c]
    # Show the filters
    img = Image.fromarray(big_img.astype('uint8'))
    img.show()

def show_kernels(saver, result_dir, num_iterations, kernel_width,
             num_kernels):
    """Loads the network and calls display_kernels_on_grid."""
    with tf.Session() as sess:
        saver.restore(sess, result_dir + 'weights-' + str(num_iterations))
        with tf.variable_scope('hidden0'):
            tf.get_variable_scope().reuse_variables()
            weights = tf.get_variable('weights')
            display_kernels_on_grid (weights.eval(), kernel_width, num_kernels)
                        
if __name__ == '__main__':
    dir_name = sys.argv[1]
    dir_name = "results/" + dir_name + "/"
    args = read_parameters(dir_name)
    step_version = read_last_iteration_number(dir_name)
    layer_info = args['Layer info'].split()
    hold2 = layer_info[0].split("-")
    args = hold2[1:]
    _, _, saver, _, _, _, _, _ = build_net(layer_info)
    show_kernels(saver, dir_name, step_version, int(args[0]), int(args[1]))
