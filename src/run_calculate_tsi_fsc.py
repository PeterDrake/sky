from FscCalculator import FscCalculator
from config import *
import sys

suffix = sys.argv[1]
calc = FscCalculator(DATA_DIR, DATA_DIR + f'/tsi_masks{suffix}', DATA_DIR)
# TODO We're only doing training and validation now; eventually we'll need to do this for testing data
# The indices for the typical and dubious timestamp filename lists are different; see config.py
# TODO Should those be dictionaries with string keys instead of lists indexed by integers?
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[0], f'typical_training_tsi_fsc{suffix}.csv')
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[1], f'typical_validation_tsi_fsc{suffix}.csv')
calc.write_pixel_counts(DUBIOUS_TIMESTAMP_FILENAMES[0], f'dubious_validation_tsi_fsc{suffix}.csv')
