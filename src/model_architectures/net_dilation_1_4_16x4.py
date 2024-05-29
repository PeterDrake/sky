from tensorflow.keras import layers
from tensorflow import keras
from utils_image import *
from functools import partial

DefaultConv2D = partial(layers.Conv2D, kernel_size=3, activation='relu', kernel_initializer='he_normal', padding='same')
DefaultPool = partial(layers.MaxPooling2D, strides=(1, 1), padding='same')

def layer(previous):
    d1 = DefaultConv2D(filters=32)(previous)
    d4 = DefaultConv2D(filters=32, dilation_rage=4)(previous)
    d16 = DefaultConv2D(filters=32, dilation_rage=16)(previous)
    return layers.Concatenate()((d1, d4, d16))

inputs = keras.Input(shape=RGB_PHOTO_SIZE)
prev = inputs
for i in range(4):
    curr = layer(prev)
    prev = curr  # For next pass through loop
outputs = layers.Conv2D(filters=4, kernel_size=3, activation='softmax', padding='same')(current)
model = keras.Model(inputs, outputs)

model.summary()
