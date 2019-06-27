#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
"""
Builds the model.
"""

import tensorflow._api.v1.keras as K
from tensorflow._api.v1.keras.models import Model
from tensorflow._api.v1.keras.layers import Convolution2D, concatenate, Input, Lambda, Layer, MaxPool2D, Add
# import keras as K
# from keras.models import Model
# from keras.layers import Convolution2D, concatenate, Input, Layer, MaxPool2D, Add
from tensorflow._api.v1.keras.utils import plot_model
from train import *


class NotGreen(Layer):
	def __init__(self, batch_size=TRAINING_BATCH_SIZE, **kwargs):
		self.batch_size = batch_size
		super().__init__(**kwargs)
		self.green = tf.constant(np.full((self.batch_size, 480, 480), 4), dtype='uint8')

	def call(self, input_tensor):
		return tf.not_equal(input_tensor, self.green)

	def get_config(self):
		base_config = super().get_config()
		return base_config


class RemoveGreen(Layer):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def call(self, inputs):
		nongreen_4d = tf.stack([inputs[0], inputs[0], inputs[0], inputs[0]], axis=3)
		all_zeros = tf.zeros_like(inputs[1], dtype='float32')
		return tf.where(nongreen_4d, inputs[1], all_zeros)

	def get_config(self, **kwargs):
		base_config = super().get_config()
		return base_config


class DecidePixelColors(Layer):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def call(self, input_tensor):
		return tf.argmax(input_tensor, axis=3)

	def get_config(self):
		base_config = super().get_config()
		return base_config


def build_model():
	"""Builds and returns the network."""
	# Create the inputs to the network.
	sky_images = Input(shape=(480, 480, 3), name='SkyImages')  # sky images
	tsi = Input(shape=(480, 480), dtype='uint8', name='TSIDecisionImages')  # TSI's decision images
	# Main body of the network
	conv1 = Convolution2D(filters=64, kernel_size=(1, 1), padding='same', data_format='channels_last', activation='relu')(sky_images)
	conv2_1 = Convolution2D(filters=64, kernel_size=(1, 1), padding='same', data_format='channels_last', activation='relu')(sky_images)
	conv3_1 = Convolution2D(filters=64, kernel_size=(1, 1), padding='same', data_format='channels_last', activation='relu')(sky_images)
	conv2 = Convolution2D(filters=64, kernel_size=(3, 3), padding='same', data_format='channels_last', activation='relu')(conv2_1)
	conv3 = Convolution2D(filters=64, kernel_size=(5, 5), padding='same', data_format='channels_last', activation='relu')(conv3_1)
	maxpool1 = MaxPool2D(pool_size=(3, 3), strides=(1, 1), padding='same', data_format='channels_last')(sky_images)
	maxpool1_conv = Convolution2D(filters=64, kernel_size=(1, 1), padding='same', data_format='channels_last', activation='relu')(maxpool1)
	concat1 = concatenate([conv1, conv2, conv3, maxpool1_conv], axis=3)
	conv4 = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(concat1)
	# Determine which pixels in TSI decision image are non-green
	nongreen = NotGreen(TRAINING_BATCH_SIZE)(tsi)
	# Output of the network, where each pixel has a probability for each color, but all probabilities are zero
	# for pixels that are green in TSI decision image
	logits_without_green = RemoveGreen()([nongreen, conv4])
	# Output of the network, where the maximum logit index replaces the vector for each pixel
	decision = DecidePixelColors()(conv4)
	# Build and return the model
	model = Model(inputs=[sky_images, tsi], outputs=[logits_without_green, decision])
	return model


if __name__ == '__main__':
	np.random.seed(123)  # for reproducibility
	model = build_model()
	model.summary()
	plot_model(model, show_shapes=True, to_file='model_2_1.png')
	# print(model.get_config())