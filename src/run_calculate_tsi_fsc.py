from FscCalculator import FscCalculator
from config import *

calc = FscCalculator(DATA_DIR, DATA_DIR + f'/tsi_masks', DATA_DIR)
calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES['training'], f'typical_training_tsi_fsc.csv')
for category in ['validation', 'testing']:
    calc.write_pixel_counts(TYPICAL_TIMESTAMP_FILENAMES[category], f'typical_{category}_tsi_fsc.csv')
    calc.write_pixel_counts(DUBIOUS_TIMESTAMP_FILENAMES[category], f'dubious_{category}_tsi_fsc.csv')
