#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finds the images (in a batch from the validation set) for which the network
most disagrees with the targets and displays how the outputs and targets
disagree.

Command line arguments:
dir

dir is the results directory where the network is stored.

Created on Thu Jun 15 15:32:13 2017

@author: jeffmullins
"""

from train import build_net, load_inputs, BATCH_SIZE, load_validation_stamps
from show_output import out_to_image, read_parameters, \
    read_last_iteration_number
import numpy as np
import sys
import tensorflow as tf
from PIL import Image
from scipy import misc
import matplotlib.pyplot as plt
from show_output import show_comparison_images

def disagreement_rate(output, target):
    """Returns the proportion of pixels in output that disagree with target."""
    return np.sum((output != target).any(axis=2)) / (480 * 480)

def find_worst_results(num_worst, time_stamps, directory, step_version, layer_info):
    """Returns the the timestamps of the num_worst images for which the network
    most disagrees with the target masks."""
    _, _, saver, _, x, y, _, _ = build_net(layer_info)
    with tf.Session() as sess:
        saver.restore(sess, directory + 'weights-' + str(step_version))
        time_stamps = load_validation_stamps(BATCH_SIZE)
        rates = np.zeros(len(time_stamps))
        for i, s in enumerate(time_stamps):
            inputs = load_inputs([s])
            result = out_to_image(y.eval(feed_dict={x: inputs}))
            result = result.reshape(480, 480, 3)
            mask = read_target(s)
            rates[i] = disagreement_rate(result, mask)
        # Display a graph of accuracies
        plt.plot(np.take(rates * 100, np.flip((rates.argsort()), axis=0)))
        plt.ylabel('Percent of Pixels Incorrect')
        plt.xlabel('Image (sorted by accuracy)')
        plt.show()
        # Report the worst disagreement rates
        indices = rates.argsort()[num_worst*-1:][::-1]
        print('Worst results percentages:\t' + str(np.take(rates, indices)))
    return np.take(time_stamps, indices)

def read_target(timestamp):
    """Reads and returns the target mask corresponding to timestamps from
    the simplemask directory."""
    return np.array(misc.imread('data/simplemask/simplemask' + str(timestamp)
                                + '.png'))

def read_targets(timestamps):
    """Reads and returns the target masks corresponding to timestamps from
    the simplemask directory."""
    masks = np.empty((len(timestamps), 480, 480, 3))
    for i, s in enumerate(timestamps):
        masks[i] = read_target(s)
    return masks

def run_stamps(saver, x, y, result_dir, iteration, stamps):
    """Loads the images for the specified timestamps and runs the network
    (using saved weights for iteration) on them. Returns the output images."""
    with tf.Session() as sess:
        saver.restore(sess, result_dir + 'weights-' + str(iteration))
        inputs = load_inputs(stamps)
        outputs = out_to_image(y.eval(feed_dict={x: inputs}))
        return outputs.reshape(-1, 480, 480, 3)

def show_sky_images(timestamps):
    """Shows the input images for timestamps."""
    for s in timestamps:
        Image.fromarray(np.array(misc.imread('data/simpleimage/simpleimage' + str(s) + '.jpg'))).show()


if __name__ == '__main__':
    timestamps = load_validation_stamps(BATCH_SIZE)
    dir_name = "results/" + sys.argv[1] + "/"
    args = read_parameters(dir_name)
    step_version = read_last_iteration_number(dir_name)
    layer_info = args['Layer info'].split()
    worst_timestamps = find_worst_results(5, timestamps, dir_name, step_version, layer_info)
    print("Worst timestamps:\t" + str(worst_timestamps))
    _, _, saver, _, x, y, _, _ = build_net(layer_info)
    outputs = run_stamps(saver, x, y, dir_name, step_version, worst_timestamps)
    targets = read_targets(worst_timestamps)
    show_comparison_images(outputs, targets)
