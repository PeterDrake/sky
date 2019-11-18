"""
Builds the model.
4 convolution layers
"""

# from tensorflow._api.v1.keras.models import Model
# from tensorflow._api.v1.keras.layers import Convolution2D, concatenate, Input, Lambda, Layer, MaxPool2D, Add
import tensorflow as tf
import numpy as np
import os
import skimage.io as io
import skimage.transform as trans
import numpy as np
from tensorflow._api.v1.keras.models import *
from tensorflow._api.v1.keras.layers import *
from tensorflow._api.v1.keras.optimizers import *
from tensorflow._api.v1.keras.callbacks import ModelCheckpoint, LearningRateScheduler
from tensorflow._api.v1.keras import backend as keras

LOSSES = 'binary_crossentropy'

METRICS = ['accuracy']


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

	# Main body of the network
	conv1 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(sky_images)
	conv1 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
	pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
	conv2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)
	conv2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv2)
	pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
	conv3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool2)
	conv3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv3)
	pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
	conv4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool3)
	conv4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv4)
	drop4 = Dropout(0.5)(conv4)
	pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

	conv5 = Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool4)
	conv5 = Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv5)
	drop5 = Dropout(0.5)(conv5)

	up6 = Conv2D(512, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
		UpSampling2D(size=(2, 2))(drop5))
	merge6 = concatenate([drop4, up6], axis=3)
	conv6 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge6)
	conv6 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv6)

	up7 = Conv2D(256, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
		UpSampling2D(size=(2, 2))(conv6))
	merge7 = concatenate([conv3, up7], axis=3)
	conv7 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge7)
	conv7 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)

	up8 = Conv2D(128, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
		UpSampling2D(size=(2, 2))(conv7))
	merge8 = concatenate([conv2, up8], axis=3)
	conv8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge8)
	conv8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv8)

	up9 = Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
		UpSampling2D(size=(2, 2))(conv8))
	merge9 = concatenate([conv1, up9], axis=3)
	conv9 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge9)
	conv9 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
	conv9 = Conv2D(2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
	conv10 = Conv2D(4, 1, activation='sigmoid')(conv9)

	decision = DecidePixelColors()(conv10)

	model = Model(inputs=[sky_images], outputs=[conv10, decision]) # in outputs, , decision
	return model
