import tensorflow as tf # Ensure tf is imported
import tensorflow.keras.optimizers
import tf_keras

from BatchGenerator import *
from ExperimentLogUpdater import *
import importlib
from config import *

# 1. Define the Multi-GPU Strategy
# This tells TensorFlow to use all visible devices (the 4 GPUs allocated by Slurm)
strategy = tf.distribute.MirroredStrategy()
print(f"Number of devices being used: {strategy.num_replicas_in_sync}") # Should print 4

# Update experiment log and create empty directory for experiment results
log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, True)
log_updater.update()

# 2. Use the Strategy Scope
# Model creation and compilation MUST occur inside this context
with strategy.scope():
    # Create the network
    module = importlib.import_module('model_architectures.' + NETWORK_ARCHITECTURE)
    model = module.model

    # Compile the model
    # Note: Compilation inside the scope automatically handles distributed components.
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# Get timestamps for the data to use
with open(DATA_DIR + '/' + TYPICAL_TIMESTAMP_FILENAMES['training'], 'r') as f:
    train_stamps = [line.strip() for line in f.readlines()]
with open(DATA_DIR + '/' + TYPICAL_TIMESTAMP_FILENAMES['validation'], 'r') as f:
    val_stamps = [line.strip() for line in f.readlines()]

# Create generators for training and validation data
train_gen = BatchGenerator(train_stamps, DATA_DIR, use_no_glare_masks="no_glare" in EXPERIMENT_NAME)
val_gen = BatchGenerator(val_stamps, DATA_DIR)

# Specify callbacks to use during training (unchanged)
callbacks = [
    tf_keras.callbacks.ModelCheckpoint(log_updater.experiment_dir + '/network.keras', save_best_only=True)
]

# Train the model (unchanged, but now executes across all 4 GPUs)
history = model.fit(train_gen, epochs=TRAIN_EPOCHS, validation_data=val_gen, callbacks=callbacks, verbose=2)

# Save the history data for plotting learning curves
pd.DataFrame(history.history).to_csv(RESULTS_DIR + '/' + EXPERIMENT_NAME + '/' + 'training_history', index_label='Epoch')
