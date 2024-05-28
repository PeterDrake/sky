from tensorflow.keras import layers
from tensorflow import keras
from utils_image import *
from functools import partial

DefaultConv2D = partial(layers.Conv2D, kernel_size=3, activation='relu', kernel_initializer='he_normal', padding='same')
inputs = keras.Input(shape=RGB_PHOTO_SIZE)
h1 = DefaultConv2D(filters=64)(inputs)
h2 = DefaultConv2D(filters=64)(h1)
h3 = DefaultConv2D(filters=64)(h2)
h4 = DefaultConv2D(filters=64)(h3)
h5 = DefaultConv2D(filters=64)(h4)
h6 = DefaultConv2D(filters=64)(h5)
h7 = DefaultConv2D(filters=64)(h6)
h8 = DefaultConv2D(filters=64)(h7)
outputs = layers.Conv2D(filters=4, kernel_size=3, activation='softmax', padding='same')(h8)
model = keras.Model(inputs, outputs)

model.summary()
