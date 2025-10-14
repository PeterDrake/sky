import os
from BatchGenerator import *
from ExperimentLogUpdater import ExperimentLogUpdater
from config import *
from skimage.io import imsave
import tensorflow as tf
import importlib
import tf_keras

# 1. Define the Multi-GPU Strategy
# This tells TensorFlow to use all visible devices (the 4 GPUs allocated by Slurm)
strategy = tf.distribute.MirroredStrategy()
print(f"Number of devices being used: {strategy.num_replicas_in_sync}") # Should print 4

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
stamps = []
with open(DATA_DIR + '/' + TYPICAL_TIMESTAMP_FILENAMES[NETWORK_IMAGE_CATEGORY], 'r') as f:
    for line in f.readlines():
        stamps.append(line.strip())
with open(DATA_DIR + '/' + DUBIOUS_TIMESTAMP_FILENAMES[NETWORK_IMAGE_CATEGORY], 'r') as f:
    for line in f.readlines():
        stamps.append(line.strip())

# Load the trained model
log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, True)
model = keras.models.load_model(log_updater.experiment_dir + '/network.h5')

print('Processing {} photos'.format(len(stamps)))
for i in range(0, len(stamps), 320):
    print('Starting chunk ' + str(i) + '-' + str(i+320))
    chunk = stamps[i:i + 320]
    print(str(len(chunk)) + ' images')
    generator = BatchGenerator(chunk, DATA_DIR)
    # Produce network masks
    predictions = model.predict(generator)
    # Save the files
    for i, timestamp in enumerate(chunk):
        network_mask = one_hot_to_rgb_mask(predictions[i])
        dir = log_updater.experiment_dir + '/network_masks/' + yyyymmdd(timestamp) + '/'
        os.makedirs(dir, exist_ok=True)
        imsave(timestamp_to_network_mask_path(log_updater.experiment_dir, timestamp), network_mask)
