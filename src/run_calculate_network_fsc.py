from FscCalculator import FscCalculator
from config import *

calc = FscCalculator(DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_NAME + '/network_masks', RESULTS_DIR + '/' + EXPERIMENT_NAME)
# TODO We're only doing validation now; eventually we'll need to do this for testing data
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES['validation'], 'typical_validation_network_fsc.csv')
calc.write_pixel_counts(DUBIOUS_TIMESTAMP_FILENAMES['validation'], 'dubious_validation_network_fsc.csv')
