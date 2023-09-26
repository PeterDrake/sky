from tensorflow.keras import layers
from tensorflow import keras
from utils_image import *
from functools import partial

DefaultConv2D = partial(layers.Conv2D, kernel_size=3, activation='relu', kernel_initializer='he_normal', padding='same')
DefaultPool = partial(layers.MaxPooling2D, strides=(1, 1), padding='same')

inputs = keras.Input(shape=RGB_PHOTO_SIZE)
c1 = DefaultConv2D(filters=32)(inputs)
c2 = DefaultConv2D(filters=32)(c1)
p1 = DefaultPool(pool_size=(1, 100))(c2)
p2 = DefaultPool(pool_size=(100, 1))(c2)
cat1 = layers.Concatenate()((c2, p1, p2))
c3 = DefaultConv2D(filters=32)(cat1)
c4 = DefaultConv2D(filters=32)(c3)
cat2 = layers.Concatenate()((c4, inputs))
outputs = layers.Conv2D(filters=4, kernel_size=3, activation='softmax', padding='same')(cat2)
model = keras.Model(inputs, outputs)

model.summary()