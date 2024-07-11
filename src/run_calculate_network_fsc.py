from FscCalculator import FscCalculator
from config import *

calc = FscCalculator(DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_NAME + '/network_masks', RESULTS_DIR + '/' + EXPERIMENT_NAME)
for quality in ['typical', 'dubious']:
    calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[NETWORK_IMAGE_CATEGORY],
                            f'{quality}_{NETWORK_IMAGE_CATEGORY}_network_fsc.csv')
