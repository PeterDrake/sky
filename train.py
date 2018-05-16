#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trains the network.

Command line arguments:
job_number layer_1 ... layer_n

Examples of layer specifications with explanations:

b:conv-3-32-a
Layer b is a convolutional layer with a 3x3 kernel and 32 output channels
taking input from layer a. (The input "layer" is called "in" for this
purpose.)

b:maxpool-32-1-a
Layer b is a max-pool layer with a 32x1 receptive field taking input from
layer a.

c:concat-a-b
Layer c concatenates the outputs of layers a and b.

Created on Mon May 22 10:20:00 2017

@author: Jeff Mullins, Sean Richardson

"""

import numpy as np
from scipy import misc
import tensorflow as tf
import sys
import os
import math
import time
import pickle
import subprocess
from preprocess import BLUE, BLACK, GREEN, COLORS

# Training parameters
BATCH_SIZE = 5
LEARNING_RATE = 0.0001
TRAINING_STEPS = 100

def build_net(layer_info):
    """Builds a network given command-line layer info."""
    print("Building network")
    tf.reset_default_graph()
    b_mask = color_mask(misc.imread('data/always_black_mask.png'),
                        index_of(BLACK, COLORS))
    g_mask = color_mask(misc.imread('data/always_green_mask.png'),
                        index_of(GREEN, COLORS))
    x = tf.placeholder(tf.float32, [None, 480, 480, 3])
    num_layers = len(layer_info)
    table, last_name = parse_layer_info(layer_info)
    h = {}
    h["in"] = x
    for n in range(0, num_layers-1):
        name, oper = get_name_oper(layer_info[n])
        if (oper == 'conv'):
            h[name] = convo_layer(table[name]["ins"],
                                  table[name]["outs"],
                                  table[name]["kernel"],
                                  h[table[name]["prev"]],
                                  table[name]["tf_name"])
        if (oper == 'maxpool'):
            h[name] = max_pool_layer(h[table[name]["prev"]],
                                     table[name]["pool_width"],
                                     table[name]["pool_height"],
                                     name)
        if (oper == 'concat'):
                h[name] = tf.concat([h[table[name]["prev_1"]],
                                     h[table[name]["prev_2"]]], 3)
    h[last_name] = convo_layer(table[last_name]["ins"],
                               table[last_name]["outs"],
                               table[last_name]["kernel"],
                               h[table[last_name]["prev"]],
                               table[last_name]["tf_name"], False)
    m = mask_layer(h[last_name], b_mask, g_mask)
    y = tf.reshape(m, [-1, 5])
    y_ = tf.placeholder(tf.int64, [None])
    cross_entropy = tf.reduce_mean(
        tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y, 1), y_)
    saver = tf.train.Saver()
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    init = tf.global_variables_initializer()    
    return train_step, accuracy, saver, init, x, y, y_, cross_entropy

def check_for_commit():
    """Raises an exception if the git state is not clean. This ensures that
    any experiment is run from code in one specific commit."""
    label = subprocess.check_output(["git", "status", "--untracked-files=no",
                                     "--porcelain"])
    if (str(label).count('\\n') != 0):
        raise Exception('Not in clean git state\n')

def color_mask(img, i):
    """Takes a boolean mask and returns an image of one-hot vectors.
    Each vector is all zeroes, except that the ith element of pixels that
    are not BLUE in img is 1e7. This results in a "mask" that can be
    added to the output of a network layer, overwhelming that layer's
    normal output to dominate softmax."""
    r, c = img.shape[:-1]
    bool_mask = np.zeros((r, c), dtype=bool)
    bool_mask[(img != BLUE).any(axis=2)] = True
    result = np.zeros((r, c, 5), dtype=np.float32)
    result[bool_mask, i] = 1e7
    return result

def conv2d(x, W, layer_num):
    """Returns a 2D convolutional layer with weights W. (Biases are added
    later.)"""
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME',
                        name = 'conv'+str(layer_num))

def convo_layer(num_in, num_out, width, prev, name, relu=True):
    """Returns a TensorFlow convolutional layer with the specified width,
    taking input from prev."""
    num_in, num_out, width = int(num_in), int(num_out), int(width)
    with tf.variable_scope(name):
        initial = tf.truncated_normal([width, width, num_in, num_out],
                                      stddev=(2 / math.sqrt(width * width * num_in)))
        W = tf.get_variable("weights", initializer=initial)
        initial = tf.constant(0.1, shape=[num_out])
        b = tf.Variable(initial, name='biases')
        if relu:
            h = tf.nn.relu(conv2d(prev, W, name) + b)
        else:
            h = conv2d(prev, W, name) + b   
    return h

def get_name_oper(layer):
    """Returns the name and operator from a command-line layer
    specification."""
    hold = layer.split(":")
    name = hold[0]
    oper = hold[1].split("-")[0]
    return name, oper

def index_of(x, sequence):
    """Returns the index of x in sequence. We can't figure out how to do this
    more directly; the standard index method doesn't work when x is a numpy
    array."""
    for i, item in enumerate(sequence):
        if (item == x).all():
            return i
    
def load_inputs(stamps):
    """Returns a tensor of images specified by stamps. Dimensions are: image,
    row, column, color."""
    inputs = np.empty((len(stamps), 480, 480, 3))
    for i, s in enumerate(stamps):
        inputs[i] = np.array(misc.imread('data/simpleimage/simpleimage' +
                             str(s) + '.jpg'))
    return inputs

def load_masks(stamps):
    """Returns a tensor of correct label categories (i.e., indices into
    preprocess.COLORS) for each pixel in each image specified by stamps.
    Dimensons are image, row, column. The tensor has been flattened into a
    single vector."""
    masks = np.empty((len(stamps), 480, 480))
    for i, s in enumerate(stamps):
        masks[i] = mask_to_index(np.array(
                   misc.imread('data/simplemask/simplemask'
                               + str(s) + '.png')))
    return masks.reshape((-1))

def load_validation_batch(n):
    """Returns the inputs and correct outputs for the first n validation
    examples."""
    valid_stamps = load_validation_stamps(n)
    valid_inputs = load_inputs(valid_stamps)
    valid_correct = load_masks(valid_stamps)
    return valid_inputs, valid_correct

def load_validation_stamps(n):
    """Reads the valid.stamps file in data and returns a list of the first
    n stamps."""
    with open('data/valid.stamps', 'rb') as f:
        return pickle.load(f)[:n]
    
def mask_layer(last_layer, b_mask, g_mask):
    """Returns a TensorFlow layer that adds last_layer, b_mask, and g_mask.
    Since these masks contain large values at pixels where the correct
    answer is always black or green (respectively), the output of this layer
    has those pixels colored correcly."""
    black = tf.constant(b_mask)
    green = tf.constant(g_mask)
    return tf.add(green, tf.add(black, last_layer))

def mask_to_index(img):
    """Returns a new version of img with an index (in COLORS)
    for each pixel."""
    result = np.ndarray(shape=[img.shape[0], img.shape[1]])
    for i in range(len(COLORS)):
        result[(img == COLORS[i]).all(axis=2)] = i
    return result

def max_pool_layer(prev, width, height, name):
    """Returns a TensorFlow max_pool layers of the specified width and height,
    taking input from prev."""
    width, height = int(width), int(height)
    return tf.nn.max_pool(prev,[1, width, height, 1], strides=[1, 1, 1, 1],
                          padding='SAME', name=name)

def parse_layer_info(layer_info):
    """Parses layer info from the command line. layer_info is a list of
    strings like 'f:conv-3-32-e', which says that layer f is a convolutional
    layer with a 3x3 kernel and 32 output channels taking input from layer
    e. Returns two values: a dictionary associating layer names with their
    information and the name of the last layer."""
    # The input "layer" has 3 output channels (rgb)
    table = {'in':{'outs':3}}
    count = 0
    name = ''
    for layer in layer_info:
        name, oper = get_name_oper(layer)
        args = layer.split(':')[1].split('-')[1:]
        info = {}
        # Convolutional layer
        # name:conv-width-outs-prev
        if oper == 'conv' :
            kernel = args[0]
            outs = args[1]
            tf_name = name
            if count == 0:
                ins = 3
                # First hidden layer layer is always named hidden0 so that
                # show_kernels can find it.
                tf_name = "hidden0"
            else:
                ins = table[args[2]]['outs']
            prev_name = args[2]    
            info = {"outs":outs, "ins":ins, "kernel":kernel,
                    "prev":prev_name, "tf_name":tf_name}
        # Max-pool layer
        # name:maxpool-width-height-prev
        if oper == 'maxpool' :
            pool_width = args[0]
            pool_height = args[1]
            outs = (table[args[2]])["outs"]
            prev_name = args[2]
            info = {"outs":outs, "pool_width":pool_width,
                    "pool_height":pool_height, "prev":prev_name}
        # Concatenation layer
        # name:concat-prev1-prev2
        if oper == 'concat' :
            outs = str(int(table[args[0]]["outs"]) +
                       int(table[args[1]]["outs"]))
            prev_1 = args[0]
            prev_2 = args[1]
            info = {"outs":outs, "prev_1":prev_1, "prev_2":prev_2}
        # Update table so that it can be referred to by later layers
        table[name] = info
        count += 1 
    return table, name

def save_params(job_number, layer_info, out_dir):
    """Write information about this experiment to a file parameters.txt in
    out_dir."""
    F = open(out_dir + 'parameters.txt', "w+")
    F.write("Job number:\t" + str(job_number) + "\n")
    F.write("Layer info:\t" + ' '.join(layer_info) + "\n")
    label = subprocess.check_output(["git", "rev-parse", "HEAD"])
    F.write("Git commit:\t" + str(label)[2:-3:] + "\n")
    F.close()

def train_net(train_step, accuracy, saver, init, x, y, y_, cross_entropy,
              valid_inputs, valid_correct, result_dir):
    """Trains the network."""
    print("Training network")
    start = time.time()
    # Get image and make the mask into a one-hotted mask
    with open('data/train.stamps', 'rb') as f:
        train_stamps = pickle.load(f)
    with open(result_dir + 'output.txt', 'w') as f:
        with tf.Session() as sess:
            init.run()
            print('Step\tTrain\tValid', file=f, flush=True)
            j = 0
            for i in range(1, TRAINING_STEPS + 1):
                j += 1
                if (j*BATCH_SIZE >= len(train_stamps)):
                    j = 1
                batch = train_stamps[(j-1) * BATCH_SIZE : j * BATCH_SIZE]
                inputs = load_inputs(batch)
                correct = load_masks(batch)
                train_step.run(feed_dict={x: inputs, y_: correct})
                if i % 10 == 0:
                    saver.save(sess, result_dir + 'weights', global_step=i)
                    train_accuracy = accuracy.eval(feed_dict={
                            x: inputs, y_: correct})
                    valid_accuracy = accuracy.eval(feed_dict={
                            x: valid_inputs, y_: valid_correct})
                    print('{}\t{:1.5f}\t{:1.5f}'.format(i,
                                                        train_accuracy,
                                                        valid_accuracy),
                          file=f,
                          flush=True)                             
        stop = time.time()  
        F = open(out_dir + 'parameters.txt', 'a')
        F.write('Elapsed time:\t' + str(stop - start) + ' seconds\n')
        F.close()


if __name__ == '__main__':
    check_for_commit()
    job_number = sys.argv[1]
    layer_info = sys.argv[2::]
    out_dir = 'results/' + job_number + '/'
    os.makedirs(out_dir)
    save_params(job_number, layer_info, out_dir)
    train_net(*build_net(layer_info),
              *load_validation_batch(BATCH_SIZE),
              out_dir)
