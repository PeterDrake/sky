#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shows the output of the network for some particular timestamp.

Command line arguments:
dir --compare --time t

dir is the results directory where the network is stored.
--compare, if specified, displays several additional images for comparsion.
--time sets the timestamp to examine to t; otherwise a default is used.

Created on Fri Jun  2 14:58:47 2017

@author: drake
"""

from train import build_net, load_inputs, load_masks
from preprocess import BLUE, WHITE, GRAY, BLACK, GREEN
import numpy as np
import tensorflow as tf
from PIL import Image
from scipy import misc
import argparse

# Time stamp of default image
TIME_STAMP = 20160414162830

# Don't show comparison images by default
SHOW_ALL = False

# BLUE_FOR_GRAY (for example) means our net gave blue when the target mask
# gave gray
BLUE_FOR_GRAY = [85, 0, 0]  # Very dark red
BLUE_FOR_WHITE = [170, 0, 0]  # Dark red
GRAY_FOR_WHITE = [255, 0, 0]  # Bright red
GRAY_FOR_BLUE = [0, 85, 0]  # Dark green
WHITE_FOR_BLUE = [0, 170, 0]  # Medium green
WHITE_FOR_GRAY = [0, 255, 0]  # Bright green

def one_hot_to_mask(max_indices, output):
    """Modifies (and returns) img to have sensible colors in place of
    one-hot vectors."""
    out = np.zeros([len(output), 480, 480 ,3])
    out[(max_indices == 0)] = WHITE
    out[(max_indices == 1)] = BLUE
    out[(max_indices == 2)] = GRAY
    out[(max_indices == 3)] = BLACK
    out[(max_indices == 4)] = GREEN
    return out

def out_to_image(output):
    """Modifies (and returns) the output of the network as a human-readable RGB
    image."""
    output = output.reshape([-1, 480, 480, 5])
    # We use argmax instead of softmax so that we really will get one-hots
    max_indexes = np.argmax(output, axis=3)
    return one_hot_to_mask(max_indexes, output)

def read_last_iteration_number(directory):
    """Reads the output.txt file in directory. Returns the iteration number
    on the last row."""
    F = open(directory + 'output.txt', 'r')
    file = F.readlines()
    line = file[len(file) - 1]
    return (line.split()[0])

def read_parameters(directory):
    """Reads the parameters.txt file in directory. Returns a dictionary
    associating labels with keys."""
    F = open(directory + 'parameters.txt', 'r')
    file = F.readlines()
    args = {}
    for line in file:
        key, value = line.split(':\t')
        args[key] = value
    return args

def show_comparison_images(outputs, targets):
    """Shows images of where outputs differ from targets, color-coded by how
    they agree or disagree. Destructively modifies targets."""
    targets[np.logical_and((outputs == BLUE).all(axis=3),
                           (targets == GRAY).all(axis=3))] = BLUE_FOR_GRAY
    targets[np.logical_and((outputs == BLUE).all(axis=3),
                           (targets == WHITE).all(axis=3))] = BLUE_FOR_WHITE
    targets[np.logical_and((outputs == GRAY).all(axis=3),
                           (targets == BLUE).all(axis=3))] = GRAY_FOR_BLUE
    targets[np.logical_and((outputs == GRAY).all(axis=3),
                           (targets == WHITE).all(axis=3))] = GRAY_FOR_WHITE
    targets[np.logical_and((outputs == WHITE).all(axis=3),
                           (targets == BLUE).all(axis=3))] = WHITE_FOR_BLUE
    targets[np.logical_and((outputs == WHITE).all(axis=3),
                           (targets == GRAY).all(axis=3))] = WHITE_FOR_GRAY
    for i in range(targets.shape[0]):
        disp = Image.fromarray(targets[i].astype('uint8'))
        disp.show()

def show_output(accuracy, saver, x, y, y_, result_dir, num_iterations, time,
             show_all):
    """Loads the network and displays the output for the specified time. Returns
    the network output."""
    with tf.Session() as sess:
        saver.restore(sess, result_dir + 'weights-' + str(num_iterations))
        inputs = load_inputs([TIME_STAMP])
        result = y.eval(feed_dict={x: inputs})
        img = out_to_image(result)[0]
        if (show_all):
            mask = np.array(misc.imread('data/simplemask/simplemask' + str(time) + '.png'))
            Image.fromarray(inputs[0].astype('uint8')).show()
            Image.fromarray(mask.astype('uint8')).show()
            show_comparison_images(img, mask)
        img = Image.fromarray(img.astype('uint8'))
        img.show()
        img.save(result_dir + 'net-output.png')
        accuracy = accuracy.eval(feed_dict={x: inputs, y_: load_masks([time])})
        print('Accuracy = ' + str(accuracy))
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('--compare', help='If typed, images used to compare output will be displayed', action='store_true')
    parser.add_argument('--time', help='Sets the time stamp to be loaded', type=int)
    args = parser.parse_args()
    time = TIME_STAMP
    show_all = SHOW_ALL
    if args.time:
        time = args.time
    if args.compare:
        show_all = True
    dir_name = "results/" + args.directory + "/"        
    args = read_parameters(dir_name)
    step_version = read_last_iteration_number(dir_name)
    layer_info = args['Layer info'].split()
    _, accuracy, saver, _, x, y, y_, _ = build_net(layer_info) 
    show_output(accuracy, saver, x, y, y_, dir_name, step_version, time, show_all)

