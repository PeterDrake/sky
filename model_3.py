"""
Builds the model.
4 convolution layers
"""

from tensorflow._api.v1.keras.models import Model
from tensorflow._api.v1.keras.layers import Convolution2D, concatenate, Input, Lambda, Layer, MaxPool2D, Add
import tensorflow as tf

LOSSES = {
	"conv2d_3": "categorical_crossentropy",
}

METRICS = {
	"conv2d_3": 'accuracy',
}


class DecidePixelColors(Layer):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def call(self, input_tensor):
		return tf.argmax(input_tensor, axis=3)

	def get_config(self):
		base_config = super().get_config()
		return base_config


def build_model():
	"""Builds and returns the network."""

	# Create the inputs to the network.
	sky_images = Input(shape=(480, 480, 3), name='SkyImages')  # sky images
	# tsi = Input(shape=(480, 480), dtype='int64', name='TSIDecisionImages')  # TSI's decision images

	# Main body of the network
	conv1 = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(sky_images)
	maxpool1 = MaxPool2D(pool_size=(1, 100), strides=(1, 1), padding='same', data_format='channels_last')(conv1)
	maxpool2 = MaxPool2D(pool_size=(100, 1), strides=(1, 1), padding='same', data_format='channels_last')(conv1)
	concat1 = concatenate([conv1, maxpool1], axis=3)
	concat2 = concatenate([maxpool2, concat1], axis=3)
	conv2 = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(concat2)
	conv3 = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(conv2)
	concat3 = concatenate([conv3, sky_images], axis=3)
	conv4 = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu')(concat3)

	decision = DecidePixelColors()(conv4)

	model = Model(inputs=[sky_images], outputs=[conv4, decision]) # in outputs, , decision
	return model
