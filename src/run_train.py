import keras.dtensor.optimizers

from BatchGenerator import *
from ExperimentLogUpdater import *
import importlib
from config import *

# Update experiment log and create empty directory for experiment results
log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, True)
log_updater.update()

# Create the network
module = importlib.import_module('model_architectures.' + NETWORK_ARCHITECTURE)
model = module.model

# Get timestamps for the data to use
with open(DATA_DIR + '/' + TYPICAL_TIMESTAMP_FILENAMES[0], 'r') as f:
    train_stamps = [line.strip() for line in f.readlines()]
with open(DATA_DIR + '/' + TYPICAL_TIMESTAMP_FILENAMES[1], 'r') as f:
    val_stamps = [line.strip() for line in f.readlines()]

# Create generators for training and validation data
train_gen = BatchGenerator(train_stamps, DATA_DIR)
val_gen = BatchGenerator(val_stamps, DATA_DIR)

# Compile the model
model.compile(optimizer=keras.dtensor.optimizers.AdamW, loss='sparse_categorical_crossentropy')

# Specify callbacks to use during training
callbacks = [
    #TODO Change from legacy .h5 format to .keras everywhere this filename appears
    # Save the model regularly, keeping only the best one
    keras.callbacks.ModelCheckpoint(log_updater.experiment_dir + '/network.h5', save_best_only=True)
]

# Train the model, doing validation at the end of each epoch
history = model.fit(train_gen, epochs=TRAIN_EPOCHS, validation_data=val_gen, callbacks=callbacks, verbose=2)

# Save the history data for plotting learning curves
pd.DataFrame(history.history).to_csv(RESULTS_DIR + '/' + EXPERIMENT_NAME + '/' + 'training_history', index_label='Epoch')
