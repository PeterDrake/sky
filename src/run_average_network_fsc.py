from FscAverager import FscAverager
from config import *

for quality in ['typical', 'dubious']:
    for category in ['validation', 'testing']:
        avg = FscAverager(RESULTS_DIR + '/' + EXPERIMENT_NAME, f'{quality}_{category}_network_fsc.csv', \
                          half_width=10, min_stamps=4, interval=5)
        avg.write_averages(f'{quality}_{category}_network_fsc_20avg.csv')
