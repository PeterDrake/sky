from tensorflow._api.v1.keras.models import Model
from tensorflow._api.v1.keras.layers import Convolution2D, concatenate, Input, Lambda
from tensorflow._api.v1.keras.utils import multi_gpu_model, to_categorical
from tensorflow.python.keras.utils.data_utils import Sequence
from train import *
from utils import *
from config import *
import pickle
import sys



class Image_Generator(Sequence):

	def __init__(self, image_filenames, label_filenames, batch_size):
		self.image_filenames, self.label_filenames = image_filenames, label_filenames
		self.batch_size = batch_size

	def __len__(self):
		return int(np.floor(len(self.image_filenames) / float(self.batch_size)))

	def __getitem__(self, idx):
		x_filenames = self.image_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]
		y_filenames = self.label_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]

		sky_images = np.array([np.asarray(imageio.imread(file_name)) for file_name in x_filenames])
		tsi = np.array([np.asarray(imageio.imread(file_name)) for file_name in y_filenames])
		masks = np.empty((self.batch_size, 480, 480))

		for i in range(len(tsi)):
			masks[i] = mask_to_index(tsi[i])

		X = [sky_images, masks]
		Y = to_categorical(masks)
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


def build_model():
	# Create the inputs to the network.
	sky_images = Input(shape=(480, 480, 3), name='sky_image')
	# Main body of the network
	conv1 = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(sky_images)
	maxpool1 = Lambda(lambda x: tf.nn.max_pool(conv1, [1, 1, 100, 1], strides=[1, 1, 1, 1], padding='SAME'), name='maxpool1')(conv1)
	concat1 = concatenate([conv1, maxpool1], axis=3)
	conv3 = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(concat1)
	# always_full = tf.constant([[[0, 0, 0, 1] for i in range(480)] for j in range(480)], dtype='float32')
	# masked = Lambda(lambda x: tf.add(always_full, conv3), name='masked')(conv3)
	# Build and return the model
	model = Model(inputs=sky_images, outputs=conv3)
	# model = multi_gpu_model(model, gpus=2)
	return model


if __name__ == '__main__':
	with tf.device('/gpu:3'):
		np.random.seed(123)  # for reproducibility
		run_name = sys.argv[0:]


		with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
			train_stamps = pickle.load(f)
		print('Training stamps loaded.')
		with open(TYPICAL_VALID_FILE, 'rb') as f:
			valid_stamps = pickle.load(f)
		print('Validation stamps loaded.')

		training_image_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, False)
		print('Training image file paths loaded.')
		training_tsi_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, True)
		print('Training mask file paths loaded.')
		validation_image_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, False)
		print('Validation image file paths loaded.')
		validation_tsi_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, True)
		print('Validation mask file paths loaded.')

		model = build_model()
		print('Model built.')
		model.compile(optimizer='adam', loss='categorical_crossentropy')
		print('Model compiled.')

		training_batch_generator = Image_Generator(training_image_filenames, training_tsi_filenames, TRAINING_BATCH_SIZE)
		print('Training generator initialized.')
		validation_batch_generator = Image_Generator(validation_image_filenames, validation_tsi_filenames,
													 TRAINING_BATCH_SIZE)
		print('Validation generator initialized.')

		model.summary()

		model.fit_generator(generator=training_batch_generator,
							steps_per_epoch=(len(train_stamps) // (TRAINING_BATCH_SIZE)),
							epochs=1,
							verbose=1,
							validation_data=validation_batch_generator,
							validation_steps=(len(valid_stamps) // (TRAINING_BATCH_SIZE)),
							use_multiprocessing=False)

# SGE_Batch -q gpu.q -r "multi_gpu_results_2" -c "python3 multi_gpu_test_v2.py multi_gpu_results_2" -P 10
