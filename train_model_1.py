#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
# used code from train.py at the Sky repository
# used code from https://medium.com/datadriveninvestor/keras-training-on-large-datasets-3e9d9dbc09d4
"""
Trains the model.
"""

from tensorflow._api.v1.keras.utils import to_categorical
from tensorflow.python.keras.utils.data_utils import Sequence
from tensorflow._api.v1.keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflow._api.v1.keras as K
import tensorflow as tf
import numpy as np
from model_1 import build_model
from utils import *
from config import *
from train import mask_to_index
import pickle
import sys


class Image_Generator(Sequence):
	""" Creates a generator that fetches the batches of data. """

	def __init__(self, image_filenames, label_filenames, batch_size):
		self.image_filenames, self.label_filenames = image_filenames, label_filenames
		self.batch_size = batch_size

	def __len__(self):
		# return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))
		return int(np.floor(len(self.image_filenames) / float(self.batch_size)))


	def __getitem__(self, idx):
		''' Grabs the correct image and label image files for the batch. '''
		x_filenames = self.image_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]
		y_filenames = self.label_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]

		''' Makes an array of arrays where each element is an image in numpy array format. '''
		sky_images = np.array([np.asarray(imageio.imread(file_name)) for file_name in x_filenames])
		''' Makes an array of arrays where each element is an label image in numpy array format.'''
		tsi = np.array([np.asarray(imageio.imread(file_name)) for file_name in y_filenames])

		''' Converts each pixel label to a number based on color; key is found in utils. WHITE is 0, BLUE is 1, 
		GRAY is 2, BLACK is 3, and GREEN is 4.'''
		masks = np.empty((self.batch_size, 480, 480))
		for i in range(len(tsi)):
			masks[i] = mask_to_index(tsi[i])

		X = [sky_images, masks]

		''' Converts each pixel label to an array where the index indicates what color and a 1 indicates that the 
		pixel is that color. The array for each pixel should only have one 1 and the other elements should be zeros. 
		The array is now of the size (batch_size)x480x480x5. '''
		Y = to_categorical(masks)

		''' Slices off the final index of the final dimension which indicates the color green. 
		The array is now of the size (batch_size)x480x480x4. '''
		Y = Y[:, :, :, 0:4]

		return X, Y


def corrected_accuracy(y_true, y_pred):
	green = tf.constant([[0 for i in range(480)] for j in range(480)], dtype='float32')
	mask = tf.not_equal(tf.reduce_sum(y_true, axis=-1), green)
	correct = tf.cast(tf.equal(tf.argmax(tf.boolean_mask(y_true, mask), axis=-1), tf.argmax(tf.boolean_mask(y_pred, mask), axis=-1)), tf.float32)
	return tf.count_nonzero(correct)/tf.size(correct, out_type=tf.dtypes.int64)


def load_filenames(stamps, input_dir, masks):
	filenames = []
	if masks:
		for s in stamps:
			filenames.append(extract_mask_path_from_time(s, input_dir))
	else:
		for s in stamps:
			filenames.append(extract_img_path_from_time(s, input_dir))
	return filenames


if __name__ == '__main__':
	run_name = sys.argv[0:]

	with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
		train_stamps = pickle.load(f)
	print('Training stamps loaded.')
	with open(TYPICAL_VALID_FILE, 'rb') as f:
		valid_stamps = pickle.load(f)
	print('Validation stamps loaded.')

	training_image_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, False)
	print('Training image file paths loaded.')
	print(len(training_image_filenames))
	training_tsi_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, True)
	print('Training mask file paths loaded.')
	print(len(training_tsi_filenames))
	validation_image_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, False)
	print('Validation image file paths loaded.')
	validation_tsi_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, True)
	print('Validation mask file paths loaded.')

	losses = {
		"logits_without_green": "categorical_crossentropy",
	}

	metrics = {
		"logits_without_green": corrected_accuracy,
	}

	run_opts = tf.RunOptions(report_tensor_allocations_upon_oom=True)

	model = build_model()
	print('Model built.')
	model.compile(optimizer='adam', loss=losses, metrics=metrics, options=run_opts)
	print('Model compiled.')

	training_batch_generator = Image_Generator(training_image_filenames, training_tsi_filenames, TRAINING_BATCH_SIZE)
	print('Training generator initialized.')
	validation_batch_generator = Image_Generator(validation_image_filenames, validation_tsi_filenames, TRAINING_BATCH_SIZE)
	print('Validation generator initialized.')

	cb_1 = EarlyStopping(monitor='val_loss')

	model.summary()

	model.fit_generator(generator=training_batch_generator,
						steps_per_epoch=(len(train_stamps) // (TRAINING_BATCH_SIZE)),
						epochs=2,
						verbose=1,
						validation_data=validation_batch_generator,
						validation_steps=(len(valid_stamps) // (TRAINING_BATCH_SIZE)),
						use_multiprocessing=False,
						callbacks=[cb_1])

	model.save('model_1_2.h5')

