#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Anna Schall
# started 6/4/19
# used code from train.py at the Sky repository
# used code from https://medium.com/datadriveninvestor/keras-training-on-large-datasets-3e9d9dbc09d4
"""
Trains the model.
"""

from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.utils.data_utils import Sequence
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, LambdaCallback, Callback
from utils import *
import os
from config import *
import importlib
import pickle
import subprocess
import time
import sys
import tensorflow as tf
# tf.compat.v1.disable_v2_behavior() # needs to be enabled to make the current version of model work


def mask_to_index(img):
    """Returns a new version of img with an index (in COLORS) for each pixel."""
    result = np.ndarray(shape=[img.shape[0], img.shape[1]])  # TODO Simpler with a slice?
    for i in range(len(COLORS)):
        result[(img == COLORS[i]).all(axis=2)] = i
    return result


class ImageGenerator(Sequence):
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
        # TODO Avoid the confusing terminology "label image"; establish consistent terminology
        ''' Makes an array of arrays where each element is a label image in numpy array format.'''
        tsi = np.array([np.asarray(imageio.imread(file_name)) for file_name in y_filenames])
        ''' Converts each pixel label to a number based on color; key is found in utils.COLORS.'''
        masks = np.empty((self.batch_size, 480, 480))
        for i in range(len(tsi)):
            masks[i] = mask_to_index(tsi[i])
        X = [sky_images]
        # TODO Rewrite the comment below using the term one-hot
        ''' Converts each pixel label to an array where the index indicates what color and a 1 indicates that the 
        pixel is that color. The array for each pixel should only have one 1 and the other elements should be zeros. 
        The array is now of the size (batch_size)x480x480x5. '''
        Y = to_categorical(masks)
        ''' Slices off the final index of the final dimension which indicates the color green. 
        The array is now of the size (batch_size)x480x480x4. '''
        Y = Y[:, :, :, 0:4]
        return X, Y


# TODO Needs a comment
def load_filenames(stamps, input_dir, masks):
    filenames = []
    if masks:
        for s in stamps:
            filenames.append(extract_mask_path_from_time(s, input_dir))
    else:
        for s in stamps:
            filenames.append(extract_img_path_from_time(s, input_dir))
    return filenames


def save_params(job_number, out_dir):
    """Write information about this experiment to a file parameters.txt in out_dir."""
    with open(out_dir + 'parameters.txt', "w+") as f:
        f.write("Job number:\t" + str(job_number) + "\n")
        label = subprocess.check_output(["git", "rev-parse", "HEAD"])
        f.write("Git commit:\t" + str(label)[2:-3:] + "\n")


if __name__ == '__main__':
    out_dir = RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/' + MODEL_TYPE + '/'
    os.makedirs(out_dir, exist_ok=True)
    save_params(EXPERIMENT_LABEL, out_dir)
    start = time.time()
    with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
        train_stamps = pickle.load(f)
    print('Training stamps loaded.')
    with open(TYPICAL_VALID_FILE, 'rb') as f:
        valid_stamps = pickle.load(f)
    print('Validation stamps loaded.')
    training_image_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, False)
    print('Training image file paths loaded:')
    print(len(training_image_filenames))
    training_tsi_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, True)
    print('Training mask file paths loaded:')
    print(len(training_tsi_filenames))
    validation_image_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, False)
    print('Validation image file paths loaded.')
    validation_tsi_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, True)
    print('Validation mask file paths loaded.')
    m = importlib.import_module(MODEL_TYPE)
    print("Model Type: " + MODEL_TYPE)
    model = m.build_model()
    print('Model built.')
    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='adam', loss=m.LOSSES, metrics=m.METRICS)
    print('Model compiled.')
    training_batch_generator = ImageGenerator(training_image_filenames, training_tsi_filenames, TRAINING_BATCH_SIZE)
    print('Training generator initialized.')
    validation_batch_generator = ImageGenerator(validation_image_filenames, validation_tsi_filenames,
                                                TRAINING_BATCH_SIZE)
    print('Validation generator initialized.')
    cb_1 = EarlyStopping(monitor='val_loss')
    history = model.fit_generator(generator=training_batch_generator,
                                  steps_per_epoch=len(train_stamps) // TRAINING_BATCH_SIZE, epochs=10, verbose=1,
                                  validation_data=validation_batch_generator,
                                  validation_steps=len(valid_stamps) // TRAINING_BATCH_SIZE,
                                  use_multiprocessing=False,
                                  callbacks=[cb_1])  # callbacks=[cb_1, tensorboard, json_logging_callback]
    stop = time.time()
    print('Elapsed time:\t' + str(stop - start) + ' seconds')
    with open(out_dir + 'parameters.txt', 'a') as f:
        f.write('Elapsed time:\t' + str(stop - start) + ' seconds\n')
        f.write('Training Batch Size:\t' + str(TRAINING_BATCH_SIZE) + '\n')
        f.write('Number of Batches:\t' + str(NUM_TRAINING_BATCHES) + '\n')
        f.write('Learning rate:\t' + str(LEARNING_RATE) + '\n')
    model.save(MODEL_TYPE + '.h5')  # TODO Where is this file saved?
