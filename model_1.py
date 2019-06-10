#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
"""
Builds the model.
"""

from keras.models import Model
from keras.layers import Convolution2D, concatenate, Input, Lambda
from keras.utils import plot_model, multi_gpu_model
import tensorflow as tf
from config import *
from train import *


def build_model():
	"""Builds the network created by Jeff and Sean."""

	''' Create the black mask to be added to the output of the third convolutional layer. '''
	b_mask = color_mask(np.asarray(imageio.imread(TYPICAL_DATA_DIR + '/always_black_mask.png')), index_of(BLACK, COLORS))
	black = tf.constant(b_mask)

	''' Create the inputs to the network. '''
	sky_images = Input(shape=(480, 480, 3), name='SkyImages')
	tsi = Input(shape=(480, 480), dtype='int64', name='TSIDecisionImages')

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

	''' Makes a boolean array with all the pixels that are not green set to true. 
	Necessary because of the green lines on the TSI decision image.'''
	nongreen_layer = Lambda(lambda x: tf.not_equal(tsi, np.full((TRAINING_BATCH_SIZE, 480, 480), 4)), name='NonGreenLayer')(tsi)

	''' Takes a tensor and a boolean array (mask) and returns a tensor populated by entries in tensor corresponding to 
	True values in mask. Allows us to ignore the pixels where the green lines are in both the TSI decision image and our
	own network image.'''
	network_boolean = Lambda(lambda x: tf.where(tf.stack([nongreen_layer, nongreen_layer, nongreen_layer, nongreen_layer], axis=3), mask, tf.zeros_like(mask, dtype='float32')), name='NetworkBoolean')([nongreen_layer, mask])

	model = Model(inputs=[sky_images, tsi], outputs=network_boolean)

	# model = multi_gpu_model(model, gpus=4)

	return model


if __name__ == '__main__':
	np.random.seed(123)  # for reproducibility
	model = build_model()
	model.summary()
	plot_model(model, show_shapes=True, to_file='model_1_3.png')