# This is a copy of an old version of run_process.py. In practice, this will load images from files rather than
# doing any processing.

from BatchGenerator import *
from ExperimentLogUpdater import ExperimentLogUpdater
from config import *

# TODO This repeats code from run_train
stamps = pd.read_csv('../test_data/tiny_data.csv', converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
stamps = stamps['timestamp_utc'].tolist()
train_stamps = stamps[:96]
val_stamps = stamps[96:192]

# Load the trained model
# TODO Change False to True to insist on a clean git state
log_updater = ExperimentLogUpdater(RESULTS_DIR, EXPERIMENT_NAME, False)
model = keras.models.load_model(log_updater.experiment_dir + '/network.h5')

# Create generator for validation data
# TODO We'll eventually want to put testing data in here, too
val_gen = BatchGenerator(val_stamps, '../test_data')  # TODO This should be DATA_DIR, not test_data

# Produce network masks
val_preds = model.predict(val_gen)
# TODO Should we find a way to do this without loading ALL images into memory?
# TODO What about parallelism?

# Display one
def display_mask(i):
    """Quick utility to display a model's prediction."""
    timestamp = val_stamps[i]
    network_mask = one_hot_to_rgb_mask(val_preds[i])
    fig, ax = plt.subplots(1, 2)
    tsi_mask = plt.imread('../test_data' + '/tsi_masks/' + yyyymmdd(timestamp) + '/' + timestamp + '_tsi_mask.png')
    fig.suptitle(timestamp)
    ax[0].imshow(tsi_mask)
    ax[1].imshow(network_mask)

display_mask(2)
