#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command line arguments:
dir ... --compare --time t

dir is the results directory where the network is stored.
(Supply several directory names; this program shows the result of an ensemble
of the networks defined in those directories.)

--compare, if specified, displays several additional images for comparsion.

--time sets the timestamp to examine to t; otherwise a default is used.

Created on Fri Jun  2 14:58:47 2017

@author: drake
"""

from train import build_net, load_masks
from show_output import read_parameters, read_last_iteration_number, out_to_image, show_output, TIME_STAMP, SHOW_ALL
import numpy as np
from PIL import Image
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='+')
    parser.add_argument('--compare', help='If typed, images used to compare output will be displayed', action='store_true')
    parser.add_argument('--time', help='Sets the time stamp to be loaded', type=int)
    args = parser.parse_args() 
    time = TIME_STAMP
    show_all = SHOW_ALL
    if args.time:
        time = args.time
    if args.compare:
        show_all = True
    print(args.directory)
    counts = np.zeros([480 * 480, 5])
    for d in args.directory:
        dir_name = d + "/" # Does NOT include results/ to allow shell globbing
        print(dir_name)
        args = read_parameters(dir_name)
        step_version = read_last_iteration_number(dir_name)
        layer_info = args['Layer info'].split()
        _, accuracy, saver, _, x, y, y_, _ = build_net(layer_info) 
        onehot = show_output(accuracy, saver, x, y, y_, dir_name, step_version, time, show_all)
        counts += onehot
    # Now show the ensemble image
    img = out_to_image(counts)[0]
    img = Image.fromarray(img.astype('uint8'))
    img.show()
    img.save('results/ensemble-output.png')
    # Determine final image accuracy
    correctness = np.equal(np.argmax(counts, 1), load_masks([time])).astype(float)
    print('Final accuracy: ' + str(correctness.mean()))
