#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
"""
Trains the model.
"""

import numpy as np
from keras.models import Model
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D, concatenate, Input, Lambda
from keras.utils import np_utils, plot_model
import tensorflow as tf
from matplotlib import pyplot as plt
from config import *
from train import *
from model_1 import *


def load_inputs(stamps, input_dir):
	"""Returns a tensor of images specified by stamps. Dimensions are: image, row, column, color."""
	inputs = np.empty((len(stamps), 480, 480, 3))
	for i, s in enumerate(stamps):
		inputs[i] = np.asarray(imageio.imread(extract_img_path_from_time(s, input_dir)))
	return inputs


def load_masks(stamps, input_dir):
	"""Returns a tensor of correct label categories (i.e., indices into preprocess.COLORS) for each pixel in each
	image specified by stamps. Dimensions are image, row, column. The tensor has been flattened into a single
	vector."""
	masks = np.empty((len(stamps), 480, 480))
	for i, s in enumerate(stamps):
		masks[i] = mask_to_index(np.asarray(imageio.imread(extract_mask_path_from_time(s, input_dir))))
	return masks.reshape((-1))

# with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
# 	train_stamps = pickle.load(f)
# for i in range(NUM_TRAINING_BATCHES):
# 	j += 1
# 	if j * TRAINING_BATCH_SIZE >= len(train_stamps):
# 		j = 1
# 	batch = train_stamps[(j - 1) * TRAINING_BATCH_SIZE: j * TRAINING_BATCH_SIZE]
# 	inputs = load_inputs(batch, TYPICAL_DATA_DIR)
# 	correct = load_masks(batch, TYPICAL_DATA_DIR)

model = build_model()
model.compile(optimizer='adam', loss={'Accuracy': None, 'CrossEntropy': 'categorical_crossentropy' }, metrics={'Accuracy': 'accuracy', 'CrossEntropy': None })
