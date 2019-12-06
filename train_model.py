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
from tensorflow._api.v1.keras.callbacks import EarlyStopping, ModelCheckpoint, LambdaCallback, Callback
from tensorboard import TensorBoard
from utils import *
import os
from config import *
import importlib
import matplotlib.pyplot as plt
import pickle
import subprocess
import json
import time
import sys


def mask_to_index(img):
    """Returns a new version of img with an index (in COLORS) for each pixel."""
    result = np.ndarray(shape=[img.shape[0], img.shape[1]])
    for i in range(len(COLORS)):
        result[(img == COLORS[i]).all(axis=2)] = i
    return result


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

        X = [sky_images]

        ''' Converts each pixel label to an array where the index indicates what color and a 1 indicates that the 
        pixel is that color. The array for each pixel should only have one 1 and the other elements should be zeros. 
        The array is now of the size (batch_size)x480x480x5. '''
        Y = to_categorical(masks)

        ''' Slices off the final index of the final dimension which indicates the color green. 
        The array is now of the size (batch_size)x480x480x4. '''
        Y = Y[:, :, :, 0:4]

        return X, Y


def load_filenames(stamps, input_dir, masks):
    filenames = []
    if masks:
        for s in stamps:
            filenames.append(extract_mask_path_from_time(s, input_dir))
    else:
        for s in stamps:
            filenames.append(extract_img_path_from_time(s, input_dir))
    return filenames


def save_params(job_number, layer_info, out_dir):
    """Write information about this experiment to a file parameters.txt in out_dir."""
    F = open(out_dir + 'parameters.txt', "w+")
    F.write("Job number:\t" + str(job_number) + "\n")
    F.write("Layer info:\t" + ' '.join(layer_info) + "\n")
    label = subprocess.check_output(["git", "rev-parse", "HEAD"])
    F.write("Git commit:\t" + str(label)[2:-3:] + "\n")
    F.close()


if __name__ == '__main__':
    short_run = sys.argv[1]

    out_dir = RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/' + MODEL_TYPE + '/'

    os.makedirs(out_dir, exist_ok=True)

    save_params(EXPERIMENT_LABEL, NETWORK_STRUCTURE, out_dir)

    start = time.time()

    print(short_run)

    with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
        train_stamps = pickle.load(f)
    print('Training stamps loaded.')
    with open(TYPICAL_VALID_FILE, 'rb') as f:
        valid_stamps = pickle.load(f)
    print('Validation stamps loaded.')

    if short_run == 'True':
        print('SHORT RUN SET TO TRUE.')
        train_stamps = train_stamps[0:1000]
        valid_stamps = valid_stamps[0:300]

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

    m = importlib.import_module(MODEL_TYPE)
    print(m)

    model = m.build_model()
    print('Model built.')
    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='adam', loss=m.LOSSES, metrics=m.METRICS)
    print('Model compiled.')

    training_batch_generator = Image_Generator(training_image_filenames, training_tsi_filenames, TRAINING_BATCH_SIZE)
    print('Training generator initialized.')
    validation_batch_generator = Image_Generator(validation_image_filenames, validation_tsi_filenames,
                                                 TRAINING_BATCH_SIZE)
    print('Validation generator initialized.')

    cb_1 = EarlyStopping(monitor='val_loss')

    tensorboard = TensorBoard(log_dir='./logs',
                              histogram_freq=0,
                              write_graph=True,
                              write_images=False,
                              write_batch_performance=True)

    # json_log = open(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/log_acc_and_loss.json', mode='wt', buffering=1)
    # json_logging_callback = LambdaCallback(
    # 	on_batch_begin=lambda batch, logs: print(logs),
    # 	on_batch_end=lambda epoch, logs: json_log.write(
    # 		json.dumps({'batch': float(epoch), 'loss': float(logs['conv2d_2_loss']), 'acc': float(logs['conv2d_2_acc'])}) + '\n'),
    # 	on_epoch_end=lambda epoch, logs: json_log.write(
    # 		json.dumps({'epoch': float(epoch), 'val_loss': float(logs['val_conv2d_2_loss']), 'val_acc': float(logs['val_conv2d_2_acc'])}) + '\n'),
    # 	on_train_end=lambda logs: json_log.close()
    # )

    history = model.fit_generator(generator=training_batch_generator,
                                  steps_per_epoch=len(train_stamps) // TRAINING_BATCH_SIZE, epochs=3, verbose=1,
                                  validation_data=validation_batch_generator,
                                  validation_steps=len(valid_stamps) // TRAINING_BATCH_SIZE,
                                  use_multiprocessing=False,
                                  callbacks=[cb_1, tensorboard])  # callbacks=[cb_1, tensorboard, json_logging_callback]

    with open(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/' + MODEL_TYPE + '/training_history.json', 'w') as f:
        json.dump(history.history, f)

    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/' + MODEL_TYPE + '/model_acc.png', bbox_inches='tight')

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/' + MODEL_TYPE + '/model_loss.png', bbox_inches='tight')

    stop = time.time()
    print('Elapsed time:\t' + str(stop - start) + ' seconds')
    F = open(out_dir + 'parameters.txt', 'a')
    F.write('Elapsed time:\t' + str(stop - start) + ' seconds\n')
    F.write('Training Batch Size:\t' + str(TRAINING_BATCH_SIZE) + '\n')
    F.write('Number of Batches:\t' + str(NUM_TRAINING_BATCHES) + '\n')
    F.write('Learning rate:\t' + str(LEARNING_RATE) + '\n')
    F.close()

    model.save(MODEL_TYPE + '.h5')
