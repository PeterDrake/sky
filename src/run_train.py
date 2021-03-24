import os
from tensorflow.keras import layers
from tensorflow import keras
import numpy as np
import pandas as pd

# Create the network
inputs = keras.Input(shape=(480, 480, 3))
outputs = layers.Conv2D(filters=4, kernel_size=3, activation="softmax", padding="same")(inputs)
model = keras.Model(inputs, outputs)

# model.summary()

# Temporary timestamps for manual testing
stamps = pd.read_csv('../test_data/tiny_data.csv', converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
stamps = stamps['timestamp_utc'].tolist()
train_stamps = stamps[:96]
val_stamps = stamps[96:192]

print(train_stamps)
