
from tensorflow._api.v1.keras.utils import to_categorical, CustomObjectScope
from tensorflow._api.v1.keras.initializers import glorot_uniform
from tensorflow.python.keras.utils.data_utils import Sequence
from tensorflow._api.v1.keras.callbacks import EarlyStopping, ModelCheckpoint
# from tensorflow._api.v1.keras.models import load_model
# from keras.models import load_model
import tensorflow._api.v1.keras as K
import tensorflow._api.v1.keras as K
import tensorflow as tf
import numpy as np
from model_1 import build_model, NotGreen, RemoveGreen, DecidePixelColors
from train_model_1 import corrected_accuracy
from utils import *
from config import *
from train import mask_to_index
import pickle
import sys
import pandas as pd
# from keras.utils import CustomObjectScope
# from keras.initializers import glorot_uniform


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

		placeholder = np.empty((self.batch_size, 480, 480, 4))

		X = [sky_images, masks, placeholder]

		return X


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
	short_run = sys.argv[0:]

	custom = {'NotGreen': NotGreen,
			  'RemoveGreen': RemoveGreen,
			  'DecidePixelColors': DecidePixelColors,
			  'corrected_accuracy': corrected_accuracy}

	model = tf._api.v1.keras.models.load_model('model_1_6.h5', custom_objects=custom)

	with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
		train_stamps = pickle.load(f)
	print('Training stamps loaded.')

	if short_run:
		train_stamps = train_stamps[0:100]

	training_image_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, False)
	print('Training image file paths loaded.')
	training_tsi_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, True)
	print('Training mask file paths loaded.')

	training_batch_generator = Image_Generator(training_image_filenames, training_tsi_filenames, TRAINING_BATCH_SIZE)
	print('Training generator initialized.')

	model.summary()

	# images = pd.DataFrame(columns=['name', 'prediction'])
	predictions = pd.DataFrame()

	p = model.predict_generator(training_batch_generator, steps=(len(train_stamps) // (TRAINING_BATCH_SIZE)), verbose=1)
	p = {out.name.split(':')[0]: p[i] for i, out in enumerate(model.outputs)}

	list_of_decision_images = p['decide_pixel_colors/ArgMax']

	print('Length: ')
	print(len(list_of_decision_images))
	print('Element: ')
	print(list_of_decision_images[0])

	# predictions.to_csv('predictions.csv')

	#SGE_Batch -q gpu.q -r "predictions_11" -c "python3 -u make_decision_images.py True" -P 10






