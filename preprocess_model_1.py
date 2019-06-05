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
import h5py


def load_tsi(stamps, input_dir, sess, name):
	masks = np.empty((len(stamps), 480, 480))
	for i, s in enumerate(stamps):
		masks[i] = mask_to_index(np.asarray(imageio.imread(extract_mask_path_from_time(s, input_dir))))
		print('TSI Progress: ' + str(i/len(stamps)))
	# masks.shape = (60216, 480, 480)
	f = h5py.File(name + '.h5', 'w')
	arr = f.create_dataset('mydata', (2 ** 32,), chunks=True)
	print(arr)
	masks_tensor = tf.placeholder(shape=masks.shape, dtype=tf.int64)
	non_green = tf.not_equal(masks_tensor.reshape((-1)), 4)
	sess.run(non_green, feed_dict={masks_tensor: masks})
	return tf.boolean_mask(masks, non_green)


def load_filenames(stamps, input_dir):
	filenames = []
	for s in stamps:
		filenames.append(extract_img_path_from_time(s, input_dir))
	return filenames


if __name__ == '__main__':
	start = time.clock()
	# os.mkdir('Keras-Data')
	sess = tf.Session()

	with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
		train_stamps = pickle.load(f)
	print('Training stamps loaded.')
	with open(TYPICAL_VALID_FILE, 'rb') as f:
		valid_stamps = pickle.load(f)
	print('Validation stamps loaded.')

	training_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR)
	print('Training files loaded.')
	training_tsi_labels = load_tsi(train_stamps, TYPICAL_DATA_DIR, sess)
	print('Training labels loaded.')
	validation_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR)
	print('Validation files loaded.')
	validation_tsi_labels = load_tsi(valid_stamps, TYPICAL_DATA_DIR, sess)
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