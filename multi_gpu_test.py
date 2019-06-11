#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
"""
Builds the model.
"""

from tensorflow._api.v1.keras.models import Model
from tensorflow._api.v1.keras.layers import Convolution2D, concatenate, Input, Lambda
from tensorflow._api.v1.keras.utils import plot_model, multi_gpu_model
from train import *


def build_model():
	"""Builds and returns the network."""
	# Create the inputs to the network.
	a = Input(shape=(480, 480, 3), name='a')
	# Main body of the network
	conv1 = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(a)
	maxpool1 = Lambda(lambda x: tf.nn.max_pool(conv1, [1, 1, 100, 1], strides=[1, 1, 1, 1], padding='SAME'), name='maxpool1')(conv1)
	concat1 = concatenate([conv1, maxpool1], axis=3)
	conv3 = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(concat1)
	always_black = tf.constant([[[0, 0, 0, 1] for i in range(480)] for j in range(480)], dtype='float32')
	masked = Lambda(lambda x: tf.add(always_black, conv3), name='masked')(conv3)
	# Build and return the model
	model = Model(inputs=a, outputs=masked)
	# model = multi_gpu_model(model, gpus=4)
	return model


if __name__ == '__main__':
	np.random.seed(123)  # for reproducibility
	model = build_model()
	model.summary()
	# plot_model(model, show_shapes=True, to_file='model_1_3.png')