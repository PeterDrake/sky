from tensorflow._api.v1.keras.utils import to_categorical, CustomObjectScope
from tensorflow._api.v1.keras.initializers import glorot_uniform
from tensorflow.python.keras.utils.data_utils import Sequence
from tensorflow._api.v1.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow._api.v1.keras.models import load_model
# from keras.models import load_model
import tensorflow._api.v1.keras as K
import tensorflow as tf
import numpy as np
from model_1 import build_model, DecidePixelColors
# from train_model_1 import corrected_accuracy
from utils import *
from config import *
from train_model import mask_to_index
import pickle
import sys
import pandas as pd
import imageio
from process import save_network_mask
import os


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

        # global list_of_sky_filenames
        # list_of_sky_filenames = list_of_sky_filenames + x_filenames
        # global list_of_tsi_filenames
        # list_of_tsi_filenames = list_of_tsi_filenames + y_filenames

        ''' Makes an array of arrays where each element is an image in numpy array format. '''
        sky_images = np.array([np.asarray(imageio.imread(file_name)) for file_name in x_filenames])
        ''' Makes an array of arrays where each element is an label image in numpy array format.'''
        tsi = np.array([np.asarray(imageio.imread(file_name)) for file_name in y_filenames])

        ''' Converts each pixel label to a number based on color; key is found in utils. WHITE is 0, BLUE is 1, 
		GRAY is 2, BLACK is 3, and GREEN is 4.'''
        masks = np.empty((self.batch_size, 480, 480))
        for i in range(len(tsi)):
            masks[i] = mask_to_index(tsi[i])

        # placeholder = np.empty((self.batch_size, 480, 480, 4))
        b_mask = color_mask(np.asarray(imageio.imread(TYPICAL_DATA_DIR + '/always_black_mask.png')),
                            index_of(BLACK, COLORS))
        batch_b_mask = np.array([b_mask for i in range(self.batch_size)])

        X = [sky_images, masks, batch_b_mask]

        return X


def save_network_mask(timestamp, img):
    """Saves the skymasks created by the neural network in results/experiment_label/masks/year/monthday/
	eg. results/e70-00/masks/2016/0904/ and creates filename eg. networkmask_e70-00.20160904233000.png"""
    #add error for no img
    path = RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/masks/' + time_to_year(timestamp) + '/' + time_to_month_and_day(
        timestamp) + '/'
    os.makedirs(path, exist_ok=True)
    file = 'networkmask_' + EXPERIMENT_LABEL + '.' + timestamp + '.png'
    show_skymask(img, save_instead=True, save_path=path + file)


def color_mask(img, i):
    """Takes a color mask and returns an image of one-hot vectors. Each vector is all zeroes, except that the ith
	element of pixels that are not BLUE in img is 1e7. This results in a "mask" that can be added to the output of a
	network layer, overwhelming that layer's normal output to dominate softmax."""
    r, c = img.shape[:-1]
    bool_mask = np.zeros((r, c), dtype=bool)
    bool_mask[(img != BLUE).any(axis=2)] = True
    result = np.zeros((r, c, 4), dtype=np.float32)
    result[bool_mask, i] = 1e7
    return result


def index_of(x, sequence):
    """Returns the index of x in sequence. We can't figure out how to do this more directly; the standard index method
	doesn't work when x is a numpy array."""
    for i, item in enumerate(sequence):
        if (item == x).all():
            return i


def load_filenames(stamps, input_dir, masks):
    filenames = []
    if masks:
        for s in stamps:
            filenames.append(extract_mask_path_from_time(s, input_dir))
    else:
        for s in stamps:
            filenames.append(extract_img_path_from_time(s, input_dir))
    return filenames


def numbers_to_RGB(array):
    out = np.zeros((480, 480, 3))
    out[(array == 0)] = WHITE
    out[(array == 1)] = BLUE
    out[(array == 2)] = GRAY
    out[(array == 3)] = BLACK
    out[(array == 4)] = GREEN
    return out


def network_output_exists(timestamp, path=None):
    """Returns true if the mask has already been created, false otherwise."""
    if path is None:
        path = extract_network_mask_path_from_time(timestamp, EXPERIMENT_LABEL)
    return os.path.isfile(path)


def process_network_masks(timestamps, input_dir):
    """Processes images corresponding to a list of timestamps. Saves each mask in the network directory. Does NOT
	check to make sure that the image exists. This must be done by the user before calling this method."""

    custom = {'DecidePixelColors': DecidePixelColors}
    model = tf._api.v1.keras.models.load_model(MODEL_TYPE + '.h5', custom_objects=custom)

    model.summary()

    path_img = load_filenames(timestamps, input_dir, False)
    print('Image file paths loaded.')
    path_mask = load_filenames(timestamps, input_dir, True)
    print('Mask file paths loaded.')

    img_generator = Image_Generator(path_img, path_mask, TRAINING_BATCH_SIZE)
    print('Training generator initialized.')

    p = model.predict_generator(img_generator, steps=(len(timestamps) // (TRAINING_BATCH_SIZE)), verbose=1)
    # print("P1:")
    # print(p)
    p = {out.name.split(':')[0]: p[i] for i, out in enumerate(model.outputs)}
    # print("P2: ")
    # print(p)

    list_of_decision_images = p['decide_pixel_colors/ArgMax']

    for i in range(len(list_of_decision_images)):
        img = numbers_to_RGB(list_of_decision_images[i])
        save_network_mask(timestamps[i], img)


def process(start, finish, input_dir, input_csv):
    temp = sorted(list(extract_data_from_csv(input_csv, 'timestamp_utc')))[start:finish]
    times = []
    for t in temp:
        if not network_output_exists(t, EXPERIMENT_LABEL):
            if os.path.isfile(extract_img_path_from_time(t, input_dir)):
                if os.path.getsize(extract_img_path_from_time(t, input_dir)) != 0:
                    times.append(t)
    print(times)
    process_network_masks(times, input_dir)


if __name__ == '__main__':
    s = int(sys.argv[1])  # Starting index of the timestamp in the typical_data/shcu_typical_data.csv file
    f = int(sys.argv[2])  # Final timestamp to consider
    input_dir = sys.argv[3]
    input_data_csv = sys.argv[4]
    process(s, f, input_dir, input_data_csv)
