import os
from tensorflow.keras import layers
from tensorflow import keras
import numpy as np
import pandas as pd
from BatchGenerator import *
from config import EXPERIMENT_NAME

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

train_gen = BatchGenerator(train_stamps, '../test_data')
val_gen = BatchGenerator(val_stamps, '../test_data')

# Configure the model for training.
# We use the "sparse" version of categorical_crossentropy
# because our target data is integers.
model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy")

# Update experiment log
# TODO Should the results directory be specified in config.py?
os.makedirs('../results', exist_ok=True)
log_filename = '../results/experiment_log.csv'
if os.path.isfile(log_filename):
    log = pd.read_csv(log_filename)
else:
    log = pd.DataFrame(columns=['name','date','githash','netfile','notes'])
# TODO If this experiment exists, we should overwrite instead of appending
log.loc[len(log)] = [EXPERIMENT_NAME, 'Some date', 'Some git hash', 'Some network file name', '']
log.to_csv(log_filename, index=False)

# Create directory for this experiment
experiment_directory = '../results/' + EXPERIMENT_NAME
os.makedirs(experiment_directory, exist_ok=True)

callbacks = [
    keras.callbacks.ModelCheckpoint(experiment_directory + '/network.h5', save_best_only=True)
]

# Train the model, doing validation at the end of each epoch.
epochs = 3
model.fit(train_gen, epochs=epochs, validation_data=val_gen, callbacks=callbacks)


# # Generate predictions for all images in the validation set
#
# val_gen = BatchGenerator(val_stamps, '../test_data')
# val_preds = model.predict(val_gen)
#
#
# def display_mask(i):
#     """Quick utility to display a model's prediction."""
#     mask = np.argmax(val_preds[i], axis=-1)
#     mask = np.expand_dims(mask, axis=-1)
#     plt.imshow(mask)
#     plt.colorbar()
#
# display_mask(0)
