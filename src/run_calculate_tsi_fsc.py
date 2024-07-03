from FscCalculator import FscCalculator
from config import *
import sys

suffix = sys.argv[1]
calc = FscCalculator(DATA_DIR, DATA_DIR + f'/tsi_masks{suffix}', DATA_DIR)
# TODO We're only doing training and validation now; eventually we'll need to do this for testing data
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES['training'], f'typical_training_tsi_fsc{suffix}.csv')
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES['validation'], f'typical_validation_tsi_fsc{suffix}.csv')
if suffix == '':  # Temporary, because we haven't de-glared dubious data yet
    calc.write_pixel_counts(DUBIOUS_TIMESTAMP_FILENAMES['validation'], f'dubious_validation_tsi_fsc{suffix}.csv')
