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
train_gen = BatchGenerator(train_stamps, '../test_data')  # TODO This should be DATA_DIR, not test_data
val_gen = BatchGenerator(val_stamps, '../test_data')  # TODO Same here

# Compile the model
model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy")

# Specify callbacks to use during training
callbacks = [
    # Save the model regularly, keeping only the best one
    keras.callbacks.ModelCheckpoint(log_updater.experiment_dir + '/network.h5', save_best_only=True)
]

# Train the model, doing validation at the end of each epoch
model.fit(train_gen, epochs=TRAIN_EPOCHS, validation_data=val_gen, callbacks=callbacks)
