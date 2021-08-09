import os
from BatchGenerator import *
from ExperimentLogUpdater import ExperimentLogUpdater
from config import *
from skimage.io import imsave

# Get timestamps for the data to use
val_stamps = []
with open(DATA_DIR + '/' + TYPICAL_TIMESTAMP_FILENAMES[1], 'r') as f:  # Element 1 is the validation filename
    for line in f.readlines():
        val_stamps.append(line.strip())
with open(DATA_DIR + '/' + DUBIOUS_TIMESTAMP_FILENAMES[0], 'r') as f:  # Element 0 is the validation filename
    for line in f.readlines():
        val_stamps.append(line.strip())

# Load the trained model
# TODO Change False to True to insist on a clean git state
log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, False)
model = keras.models.load_model(log_updater.experiment_dir + '/network.h5')

# Create generator for validation data
# TODO Right before publication, we'll eventually want to put test data (as opposed to validation data) in here
val_gen = BatchGenerator(val_stamps, DATA_DIR)

# Produce network masks
val_preds = model.predict(val_gen)
print(val_preds.shape)
print(val_preds.dtype)
# TODO Should we find a way to do this without loading ALL images into memory?
# TODO What about parallelism?

# Save the files
# If, for debugging purposes, we want to run this on just a few images, change val_stamps to val_stamps[:4]
for i, timestamp in enumerate(val_stamps):
    network_mask = one_hot_to_rgb_mask(val_preds[i])
    dir = log_updater.experiment_dir + '/network_masks/' + yyyymmdd(timestamp) + '/'
    os.makedirs(dir, exist_ok=True)
    imsave(timestamp_to_network_mask_path(log_updater.experiment_dir, timestamp), network_mask)
