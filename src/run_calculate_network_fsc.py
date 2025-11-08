from FscCalculator import FscCalculator
from config import *

calc = FscCalculator(DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_NAME + '/network_masks', RESULTS_DIR + '/' + EXPERIMENT_NAME)
for quality in ['typical', 'dubious']:
    if quality == 'typical':
        stamps_filename = TYPICAL_TIMESTAMP_FILENAMES[NETWORK_IMAGE_CATEGORY]
    else:
        stamps_filename = DUBIOUS_TIMESTAMP_FILENAMES[NETWORK_IMAGE_CATEGORY]
    calc.write_pixel_counts(stamps_filename,
                            f'{quality}_{NETWORK_IMAGE_CATEGORY}_network_fsc.csv')
