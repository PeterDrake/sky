#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
# used code from train.py at the Sky repository
# used code from https://medium.com/datadriveninvestor/keras-training-on-large-datasets-3e9d9dbc09d4
"""
Preprocesses data for the model.
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


def load_tsi(stamps, input_dir, name):
	masks = np.empty((len(stamps), 480, 480))
	for i, s in enumerate(stamps):
		masks[i] = mask_to_index(np.asarray(imageio.imread(extract_mask_path_from_time(s, input_dir))))
		print('TSI Progress: ' + str(i/len(stamps)))
	print('SHAPE: ')
	print(masks.shape)
	with open('Keras-Data' + '/' + name + '_tsi_masks', 'wb') as f:
		pickle.dump(masks, f)
	non_green = tf.not_equal(masks.reshape((-1)), 4)
	return tf.boolean_mask(masks, non_green)


def load_filenames(stamps, input_dir):
	filenames = []
	for s in stamps:
		filenames.append(extract_img_path_from_time(s, input_dir))
	return filenames


if __name__ == '__main__':
	start = time.clock()
	os.mkdir('Keras-Data')

	with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
		train_stamps = pickle.load(f)
	print('Training stamps loaded.')
	with open(TYPICAL_VALID_FILE, 'rb') as f:
		valid_stamps = pickle.load(f)
	print('Validation stamps loaded.')

	training_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR)
	print('Training files loaded.')
	training_tsi_labels = load_tsi(train_stamps, TYPICAL_DATA_DIR, 'training')
	print('Training labels loaded.')
	validation_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR)
	print('Validation files loaded.')
	validation_tsi_labels = load_tsi(valid_stamps, TYPICAL_DATA_DIR, 'validation')
	print('Validation labels loaded.')

	with open('Keras-Data' + '/training_filenames', 'wb') as f:
		pickle.dump(training_filenames, f)
	with open('Keras-Data' + '/training_labels', 'wb') as f:
		pickle.dump(training_tsi_labels, f)
	with open('Keras-Data' + '/validation_filenames', 'wb') as f:
		pickle.dump(validation_filenames, f)
	with open('Keras-Data' + '/validation_labels', 'wb') as f:
		pickle.dump(validation_tsi_labels, f)

	print("Finished.")
	print("Time elapsed: " + str(time.clock() - start) + " seconds.")