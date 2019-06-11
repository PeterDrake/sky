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
	sky_images = Input(shape=(480, 480, 3), name='SkyImages')
	tsi = Input(shape=(480, 480), dtype='uint8', name='TSIDecisionImages') # TSI's decision images
	# Main body of the network
	conv1 = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(sky_images)
	maxpool1 = Lambda(lambda x: tf.nn.max_pool(conv1, [1, 1, 100, 1], strides=[1, 1, 1, 1], padding='SAME'), name='maxpool1')(conv1)
	maxpool2 = Lambda(lambda x: tf.nn.max_pool(conv1, [1, 100, 1, 1], strides=[1, 1, 1, 1], padding='SAME'), name='maxpool2')(conv1)
	concat1 = concatenate([conv1, maxpool1], axis=3)
	concat2 = concatenate([maxpool2, concat1], axis=3)
	conv2 = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(concat2)
	concat3 = concatenate([conv2, sky_images], axis=3)
	conv3 = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(concat3)
	# Mask to mark pixels that are ALWAYS black to be black
	b_mask = color_mask(np.asarray(imageio.imread(TYPICAL_DATA_DIR + '/always_black_mask.png')),
						index_of(BLACK, COLORS))
	always_black = tf.constant(b_mask)
	masked = Lambda(lambda x: tf.add(always_black, conv3), name='masked')(conv3)
	# Determine which pixels in TSI decision image are non-green
	nongreen = Lambda(lambda x: tf.not_equal(tsi, np.full((TRAINING_BATCH_SIZE, 480, 480), 4)), name='nongreen')(tsi)
	# Output of the network, where each pixel has a probability for each color, but all probabilities are zero
	# for pixels that are green in TSI decision image
	logits_without_green = Lambda(lambda x: tf.where(tf.stack([nongreen, nongreen, nongreen, nongreen], axis=3), masked, tf.zeros_like(masked, dtype='float32')), name='logits_without_green')([nongreen, masked])
	# Build and return the model
	model = Model(inputs=[sky_images, tsi], outputs=logits_without_green)
	print('1-----------------------------------------------')
	model.summary()
	model = multi_gpu_model(model, gpus=2)
	print('2-----------------------------------------------')
	model.summary()
	return model


if __name__ == '__main__':
	np.random.seed(123)  # for reproducibility
	model = build_model()
	model.summary()
	# plot_model(model, show_shapes=True, to_file='model_1_3.png')