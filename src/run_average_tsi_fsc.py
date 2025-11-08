from FscAverager import FscAverager
from config import *

for quality in ['typical', 'dubious']:
    for category in ['validation', 'testing']:
        avg = FscAverager(DATA_DIR, f'{quality}_{category}_tsi_fsc.csv', half_width=10, min_stamps=4, interval=5)
        avg.write_averages(f'{quality}_{category}_tsi_fsc_20avg.csv')
