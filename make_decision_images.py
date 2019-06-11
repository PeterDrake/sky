
from tensorflow._api.v1.keras.utils import to_categorical
from tensorflow.python.keras.utils.data_utils import Sequence
from tensorflow._api.v1.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow._api.v1.keras.models import load_model
import tensorflow._api.v1.keras as K
import tensorflow._api.v1.keras as K
import tensorflow as tf
import numpy as np
from model_1 import build_model
from utils import *
from config import *
from train import mask_to_index
import pickle
import sys
import pandas as pd


class Image_Generator(Sequence):
	""" Creates a generator that fetches the batches of data. """

	def __init__(self, image_filenames, batch_size):
		self.image_filenames = image_filenames
		self.batch_size = batch_size

	def __len__(self):
		return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))

	def __getitem__(self, idx):
		''' Grabs the correct image and label image files for the batch. '''
		x_filenames = self.image_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]

		''' Makes an array of arrays where each element is an image in numpy array format. '''
		sky_images = np.array([np.asarray(imageio.imread(file_name)) for file_name in x_filenames])

		return sky_images


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
	model = load_model('model_1_2.h5')

	with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
		train_stamps = pickle.load(f)
	print('Training stamps loaded.')

	training_image_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, False)
	print('Training image file paths loaded.')

	training_batch_generator = Image_Generator(training_image_filenames, TRAINING_BATCH_SIZE)
	print('Training generator initialized.')

	model.summary()

	images = pd.DataFrame(columns=['name', 'prediction'])

	predictions = model.predict_generator(training_batch_generator, steps=(len(train_stamps) // (TRAINING_BATCH_SIZE)))







