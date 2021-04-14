from tensorflow.keras import layers
from tensorflow import keras

inputs = keras.Input(shape=(480, 480, 3))
outputs = layers.Conv2D(filters=4, kernel_size=3, activation='softmax', padding='same')(inputs)
model = keras.Model(inputs, outputs)
