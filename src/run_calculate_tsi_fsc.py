from FscCalculator import FscCalculator
from config import *

calc = FscCalculator(DATA_DIR, DATA_DIR + '/tsi_masks', DATA_DIR)
# TODO We're only doing validation now; eventually we'll need to do this for testing data
# The indices 1 and 0 below indicate the validation set
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[1], 'typical_validation_tsi_fsc.csv')
calc.write_pixel_counts(DUBIOUS_TIMESTAMP_FILENAMES[0], 'dubious_validation_tsi_fsc.csv')
