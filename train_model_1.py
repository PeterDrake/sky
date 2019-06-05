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

	def __init__(self, image_filenames, label_filenames, batch_size):
		self.image_filenames, self.label_filenames = image_filenames, label_filenames
		self.batch_size = batch_size

	def __len__(self):
		return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))

	def __getitem__(self, idx):
		x_filenames = self.image_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]
		y_filenames = self.label_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]

		sky_images = np.array([np.asarray(imageio.imread(file_name)) for file_name in x_filenames])
		tsi = np.array([np.asarray(imageio.imread(file_name)) for file_name in y_filenames])

		X = [sky_images, tsi]

		masks = np.empty((self.batch_size, 480, 480))
		for i in range(len(tsi)):
			masks[i] = mask_to_index(tsi[i])
		m = masks.reshape((-1))
		m_ = tf.convert_to_tensor(m, dtype=tf.int64)
		non_green = tf.not_equal(m_, 4)
		Y = tf.boolean_mask(m_, non_green)
		return X, Y


# def load_tsi(stamps, input_dir):
# 	masks = np.empty((len(stamps), 480, 480))
# 	for i, s in enumerate(stamps):
# 		masks[i] = mask_to_index(np.asarray(imageio.imread(extract_mask_path_from_time(s, input_dir))))
# 	non_green = tf.not_equal(masks.reshape((-1)), 4)
# 	return tf.boolean_mask(masks, non_green)


def load_filenames(stamps, input_dir, masks):
	filenames = []
	if masks:
		for s in stamps:
			filenames.append(extract_mask_path_from_time(s, input_dir))
	else:
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
	print('Training stamps loaded.')
	with open(TYPICAL_VALID_FILE, 'rb') as f:
		valid_stamps = pickle.load(f)
	print('Validation stamps loaded.')

	training_image_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, False)
	print('Training image file paths loaded.')
	training_tsi_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, True)
	print('Training mask file paths loaded.')
	validation_image_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, False)
	print('Validation image file paths loaded.')
	validation_tsi_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, True)
	print('Validation mask file paths loaded.')

	model = build_model()
	print('Model built.')
	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
	print('Model compiled.')

	training_batch_generator = Image_Generator(training_image_filenames, training_tsi_filenames, TRAINING_BATCH_SIZE)
	print('Training generator initialized.')
	validation_batch_generator = Image_Generator(validation_image_filenames, validation_tsi_filenames, TRAINING_BATCH_SIZE)
	print('Validation generator initialized.')

	model.fit_generator(generator=training_batch_generator,
						steps_per_epoch=(len(train_stamps) // TRAINING_BATCH_SIZE),
						epochs=2,
						verbose=1,
						validation_data=validation_batch_generator,
						validation_steps=(len(valid_stamps) // TRAINING_BATCH_SIZE),
						use_multiprocessing=False)

	# SGE_Batch -q gpu.q -r "keras_train_1" -c "python3 train_model_1.py" -P 10
