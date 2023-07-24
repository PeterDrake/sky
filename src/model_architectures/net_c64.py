from tensorflow.keras import layers
from tensorflow import keras
from utils_image import *

inputs = keras.Input(shape=RGB_PHOTO_SIZE)
h1 = layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same')(inputs)
outputs = layers.Conv2D(filters=4, kernel_size=3, activation='softmax', padding='same')(h1)
model = keras.Model(inputs, outputs)
