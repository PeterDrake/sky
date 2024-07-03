from FscCalculator import FscCalculator
from config import *

calc = FscCalculator(DATA_DIR, RESULTS_DIR + '/' + EXPERIMENT_NAME + '/network_masks', RESULTS_DIR + '/' + EXPERIMENT_NAME)
for quality in ['typical', 'dubious']:
    for category in ['validation', 'testing']:
        calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[category], f'{quality}_{category}_network_fsc.csv')
