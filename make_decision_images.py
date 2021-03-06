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

		global list_of_sky_filenames
		list_of_sky_filenames = list_of_sky_filenames + x_filenames
		global list_of_tsi_filenames
		list_of_tsi_filenames = list_of_tsi_filenames + y_filenames

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
		b_mask = color_mask(np.asarray(imageio.imread(TYPICAL_DATA_DIR + '/always_black_mask.png')), index_of(BLACK, COLORS))
		batch_b_mask = np.array([b_mask for i in range(self.batch_size)])

		X = [sky_images, masks, batch_b_mask]

		return X

def save_network_mask(timestamp, img):
	"""Saves the skymasks created by the neural network in results/experiment_label/masks/year/monthday/
	eg. results/e70-00/masks/2016/0904/ and creates filename eg. networkmask_e70-00.20160904233000.png"""
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


if __name__ == '__main__':

	custom = {'DecidePixelColors': DecidePixelColors}
	model = tf._api.v1.keras.models.load_model(MODEL_TYPE + '.h5', custom_objects=custom)

	# short_run = sys.argv[0:]
	input_dir = sys.argv[1]
	input_file_path = sys.argv[2]

	with open(input_dir + input_file_path, 'rb') as f:
		input_stamps = pickle.load(f)
	print('Stamps loaded from ' + input_file_path)

	# if short_run == 'True':
	# 	train_stamps = train_stamps[0:100]

	image_filenames = load_filenames(input_stamps, input_dir, False)
	print('Training image file paths loaded.')
	tsi_filenames = load_filenames(input_stamps, input_dir, True)
	print('Training mask file paths loaded.')

	batch_generator = Image_Generator(image_filenames, tsi_filenames, TRAINING_BATCH_SIZE)
	print('Training generator initialized.')

	# with open(TYPICAL_VALID_FILE, 'rb') as f:
	# 	valid_stamps = pickle.load(f)
	# print('Validation stamps loaded.')
	#
	# validation_image_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, False)
	# print('Validation image file paths loaded.')
	# validation_tsi_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, True)
	# print('Validation mask file paths loaded.')
	#
	# validation_batch_generator = Image_Generator(validation_image_filenames, validation_tsi_filenames, TRAINING_BATCH_SIZE)
	# print('Validation generator initialized.')

	# poster_test.stamps  poster_valid.stamps

	# with open(DUBIOUS_DATA_DIR + '/poster_test.stamps', 'rb') as f:
	# 	valid_stamps = pickle.load(f)
	# print('Dubious stamps loaded.')
	#
	# validation_image_filenames = load_filenames(valid_stamps, DUBIOUS_DATA_DIR, False)
	# print('Validation image file paths loaded.')
	# validation_tsi_filenames = load_filenames(valid_stamps, DUBIOUS_DATA_DIR, True)
	# print('Validation mask file paths loaded.')
	#
	# validation_batch_generator = Image_Generator(validation_image_filenames, validation_tsi_filenames, TRAINING_BATCH_SIZE)
	# print('Validation generator initialized.')


	model.summary()

	list_of_sky_filenames = []
	list_of_tsi_filenames = []

	# don't need ?
	# images = pd.DataFrame(columns=['name', 'prediction'])
	predictions = pd.DataFrame()

	p = model.predict_generator(batch_generator, steps=(len(input_stamps) // (TRAINING_BATCH_SIZE)), verbose=1)
	# p = model.predict_generator(validation_batch_generator, steps=(len(valid_stamps) // (TRAINING_BATCH_SIZE)), verbose=1)
	p = {out.name.split(':')[0]: p[i] for i, out in enumerate(model.outputs)}

	list_of_decision_images = p['decide_pixel_colors/ArgMax']

	# os.mkdir('Network _Decision_Images_1')

	for i in range(len(list_of_decision_images)):
		file = str(i) + '.png'
		img = numbers_to_RGB(list_of_decision_images[i])
		timestamp = extract_timestamp(list_of_sky_filenames[i])
		imageio.imwrite(file, img)
		save_network_mask(timestamp, img)

	print(list_of_sky_filenames)
	print(list_of_tsi_filenames)



# SGE_Batch -q gpu.q -r "predictions_16" -c "python3 -u make_decision_images.py False" -P 10




