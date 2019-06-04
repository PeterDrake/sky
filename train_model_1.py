#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
# used code from train.py at the Sky repository
# used code from https://medium.com/datadriveninvestor/keras-training-on-large-datasets-3e9d9dbc09d4
"""
Trains the model.
"""

import numpy as np
from keras.models import Model
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D, concatenate, Input, Lambda
from keras.utils import np_utils, plot_model, Sequence
import tensorflow as tf
from matplotlib import pyplot as plt
from config import *
from train import *
from model_1 import *


class Image_Generator(Sequence):

    def __init__(self, image_filenames, labels, batch_size):
        self.image_filenames, self.labels = image_filenames, labels
        self.batch_size = batch_size

    def __len__(self):
        return np.ceil(len(self.image_filenames) / float(self.batch_size))

    def __getitem__(self, idx):
        batch_x = self.image_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.labels[idx * self.batch_size:(idx + 1) * self.batch_size]

        return np.array([imageio.imread(file_name) for file_name in batch_x]), np.array(batch_y)


def load_tsi(stamps, input_dir):
	masks = np.empty((len(stamps), 480, 480))
	for i, s in enumerate(stamps):
		masks[i] = mask_to_index(np.asarray(imageio.imread(extract_mask_path_from_time(s, input_dir))))
	non_green = tf.not_equal(masks.reshape((-1)), 4)
	return tf.boolean_mask(masks, non_green)


def load_filenames(stamps, input_dir):
	filenames = []
	for s in stamps:
		filenames.append(extract_img_path_from_time(s, input_dir))
	return filenames


def format_tsi_masks(masks):
	non_green = tf.not_equal(masks, 4)
	return tf.boolean_mask(masks, non_green)


def create_batch_sets():
	batches = []
	j = 0
	for i in range(NUM_TRAINING_BATCHES):
		j += 1
		if j * TRAINING_BATCH_SIZE >= len(train_stamps):
			j = 1
		batches.append(train_stamps[(j - 1) * TRAINING_BATCH_SIZE: j * TRAINING_BATCH_SIZE])
	return batches


# def image_generator(stamps):
# 	while True:
# 		# batch_stamps = np.random.choice(a=stamps, size=TRAINING_BATCH_SIZE)
# 		batch_stamps = stamps
# 		batch_x = load_inputs(batch_stamps, TYPICAL_DATA_DIR)
# 		batch_y = format_tsi_masks(load_masks(batch_stamps, TYPICAL_DATA_DIR))
#
# 		yield (batch_x, batch_y)

if __name__ == '__main__':
	with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
		train_stamps = pickle.load(f)
	with open(TYPICAL_VALID_FILE, 'rb') as f:
		valid_stamps = pickle.load(f)

	training_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR)
	training_tsi_labels = load_tsi(train_stamps, TYPICAL_DATA_DIR)
	validation_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR)
	validation_tsi_labels = load_tsi(valid_stamps, TYPICAL_DATA_DIR)

	model = build_model()
	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

	training_batch_generator = Image_Generator(training_filenames, training_tsi_labels, TRAINING_BATCH_SIZE)
	validation_batch_generator = Image_Generator(validation_filenames, validation_tsi_labels, TRAINING_BATCH_SIZE)

	# model.fit_generator(generator=training_batch_generator,
	# 					steps_per_epoch=(len(train_stamps) // TRAINING_BATCH_SIZE),
	# 					epochs=2,
	# 					verbose=1,
	# 					validation_data=validation_batch_generator,
	# 					validation_steps=(len(valid_stamps) // TRAINING_BATCH_SIZE),
	# 					use_multiprocessing=True)

