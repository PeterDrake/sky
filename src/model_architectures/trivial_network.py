from tensorflow.keras import layers
from tensorflow import keras
from utils_image import *

inputs = keras.Input(shape=RGB_PHOTO_SIZE)
outputs = layers.Conv2D(filters=4, kernel_size=3, activation='softmax', padding='same')(inputs)
model = keras.Model(inputs, outputs)
