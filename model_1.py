#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
"""
Builds the model.
"""

import numpy as np
from keras.models import Model
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D, concatenate, Input, Lambda
from keras.utils import np_utils, plot_model
import tensorflow as tf
from matplotlib import pyplot as plt
from config import *
from train import *


def build_model():
	"""Builds the network created by Jeff and Sean."""

	''' Create the black mask to be added to the output of the third convolutional layer. '''
	b_mask = color_mask(np.asarray(imageio.imread(TYPICAL_DATA_DIR + '/always_black_mask.png')), index_of(BLACK, COLORS))
	black = tf.constant(b_mask)

	''' Create the inputs to the network. '''
	sky_images = Input(shape=(480, 480, 3), name='SkyImages')
	tsi = Input(shape=[None], dtype='int64', name='TSIDecisionImages')

	''' Create the main body of the network. '''
	first_conv = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='FirstConvolution')(sky_images)
	first_maxpool = Lambda(lambda x: tf.nn.max_pool(first_conv, [1, 1, 100, 1], strides=[1, 1, 1, 1], padding='SAME'), name='FirstMaxPool')(first_conv)
	second_maxpool = Lambda(lambda x: tf.nn.max_pool(first_conv, [1, 100, 1, 1], strides=[1, 1, 1, 1], padding='SAME'), name='SecondMaxPool')(first_conv)
	merge_one = concatenate([first_conv, first_maxpool], axis=3)
	merge_two = concatenate([second_maxpool, merge_one], axis=3)
	second_conv = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='SecondConvolution')(merge_two)
	merge_three = concatenate([second_conv, sky_images], axis=3)
	third_conv = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='ThirdConvolution')(merge_three)

	''' Add the always_black_mask to the output of the third convolutional layer. Calls mask_layer from train.py'''
	mask = Lambda(lambda x: tf.add(black, third_conv), name='MaskLayer')(third_conv)

	''' Flattens the mask layer. '''
	reshape_layer = Lambda(lambda x: tf.reshape(mask, [-1, 4]), name='Reshape')(mask)

	''' Makes a boolean array with all the pixels that are not green set to true. 
	Necessary because of the green lines on the TSI decision image.'''
	nongreen_layer = Lambda(lambda x: tf.not_equal(tsi, 4), name='NonGreenLayer')(tsi)

	''' Takes a tensor and a boolean array (mask) and returns a tensor populated by entries in tensor corresponding to 
	True values in mask. Allows us to ignore the pixels where the green lines are in both the TSI decision image and our
	own network image.'''
	network_boolean = Lambda(lambda x: tf.boolean_mask(reshape_layer, nongreen_layer), name='NetworkBoolean')([reshape_layer, nongreen_layer])
	tsi_boolean = Lambda(lambda x: tf.boolean_mask(tsi, nongreen_layer), name='TSIBoolean')([tsi, nongreen_layer])

	# ''' Performs Softmax Cross Entropy with Logits using network_boolean and tsi_boolean. '''
	# #find out why keras wasn't happy with Sparse Softmax Cross Entropy with Logits
	# s_s_cross_entropy_w_l = Lambda(lambda x: tf.nn.softmax_cross_entropy_with_logits(labels=tsi_boolean, logits=network_boolean), name='SparseSoftmaxCrossEntropy')([tsi_boolean, network_boolean])
	#
	# ''' Takes the average loss over the batch. '''
	# cross_entropy = Lambda(lambda x: tf.reduce_mean(s_s_cross_entropy_w_l), name='CrossEntropy')(s_s_cross_entropy_w_l)

	''' Returns the index with the largest value across the first axis of the network_boolean tensor. '''
	arg_max = Lambda(lambda x: tf.math.argmax(network_boolean, 1), name='ArgMax')(network_boolean)

	''' Returns the truth value of (arg_max == tsi_boolean) element-wise. Essentially evaluates which pixels where 
	correctly classified by the network according to the TSI decision image.'''
	correct_prediction = Lambda(lambda x: tf.equal(arg_max, tsi_boolean), name='CorrectPrediction')([arg_max, tsi_boolean])

	''' Casts the boolean tensor output of correct_prediction to float. 
	Converts False values to 0 and True values to 1. '''
	cast = Lambda(lambda x: tf.cast(correct_prediction, tf.float32), name='Cast')(correct_prediction)

	# ''' Takes the average value over the float version of correct_prediction.
	# Should return a number between 0 and 1. '''
	# accuracy = Lambda(lambda x: tf.reduce_mean(cast), name='Accuracy')(cast)

	''' Creates the model with two inputs (sky images and TSI decision images) 
	and two outputs (cross entropy loss and accuracy)'''
	# model = Model(inputs=[sky_images, tsi], outputs=[cross_entropy, accuracy])
	model = Model(inputs=[sky_images, tsi], outputs=[correct_prediction, cast])


	return model


if __name__ == '__main__':
	np.random.seed(123)  # for reproducibility
	model = build_model()
	model.summary()
	# plot_model(model, show_shapes=True, to_file='model_1.png')