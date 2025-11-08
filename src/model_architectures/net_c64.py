from tensorflow.keras import layers
from tensorflow import keras
from utils_image import *
from functools import partial

DefaultConv2D = partial(layers.Conv2D, kernel_size=3, activation='relu', kernel_initializer='he_normal', padding='same')
inputs = keras.Input(shape=RGB_PHOTO_SIZE)
h1 = DefaultConv2D(filters=64)(inputs)
outputs = layers.Conv2D(filters=4, kernel_size=3, activation='softmax', padding='same')(h1)
model = keras.Model(inputs, outputs)
