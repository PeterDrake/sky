import os
from tensorflow.keras import layers
from tensorflow import keras
import numpy as np
import pandas as pd
from BatchGenerator import *
from config import EXPERIMENT_NAME
from datetime import date
import sys
import git
from ExperimentLogUpdater import *
import importlib

# Update experiment log and create empty directory for experiment results
# TODO Change False to True to insist on a clean git state
log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, False)
log_updater.update()

# Create the network
module = importlib.import_module(NETWORK_ARCHITECTURE)
model = module.model

# Get timestamps for the data to use
# Temporary timestamps for manual testing
stamps = pd.read_csv('../test_data/tiny_data.csv', converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
stamps = stamps['timestamp_utc'].tolist()
train_stamps = stamps[:96]
val_stamps = stamps[96:192]

# Create generators for training and validation data
train_gen = BatchGenerator(train_stamps, '../test_data')
val_gen = BatchGenerator(val_stamps, '../test_data')

# Compile the model
model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy")

# Specify callbacks to use during training
callbacks = [
    # Save the model regularly, keeping only the best one
    keras.callbacks.ModelCheckpoint(log_updater.experiment_dir + '/network.h5', save_best_only=True)
]

# Train the model, doing validation at the end of each epoch
model.fit(train_gen, epochs=TRAIN_EPOCHS, validation_data=val_gen, callbacks=callbacks)


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
