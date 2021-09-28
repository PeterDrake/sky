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
for i in range(0, len(val_stamps), 320):
    print('Starting chunk ' + str(i) + '-' + str(i+320))
    chunk = val_stamps[i:i+320]
    print(str(len(chunk)) + ' images')
    val_gen = BatchGenerator(chunk, DATA_DIR)
    # Produce network masks
    val_preds = model.predict(val_gen)
    print('len(val_preds): ' + str(len(val_preds)))
    print('len(chunk): ' + str(len(chunk)))
    # Save the files
    # If, for debugging purposes, we want to run this on just a few images, change val_stamps to val_stamps[:4]
    for i, timestamp in enumerate(chunk):
        network_mask = one_hot_to_rgb_mask(val_preds[i])
        dir = log_updater.experiment_dir + '/network_masks/' + yyyymmdd(timestamp) + '/'
        os.makedirs(dir, exist_ok=True)
        imsave(timestamp_to_network_mask_path(log_updater.experiment_dir, timestamp), network_mask)
