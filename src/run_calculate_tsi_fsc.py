from FscCalculator import FscCalculator
from config import *

calc = FscCalculator(DATA_DIR, DATA_DIR + '/tsi_masks', DATA_DIR)
# TODO We're only doing training and validation now; eventually we'll need to do this for testing data
# The indices for the typical and dubious timestamp filename lists are different; see config.py
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[0], 'typical_training_tsi_fsc.csv')
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[1], 'typical_validation_tsi_fsc.csv')
calc.write_pixel_counts(DUBIOUS_TIMESTAMP_FILENAMES[0], 'dubious_validation_tsi_fsc.csv')
