from FscAverager import FscAverager
from config import *

for quality in ['typical', 'dubious']:
        avg = FscAverager(RESULTS_DIR + '/' + EXPERIMENT_NAME,
                          f'{quality}_{NETWORK_IMAGE_CATEGORY}_network_fsc.csv', \
                          half_width=10, min_stamps=4, interval=5)
        avg.write_averages(f'{quality}_{NETWORK_IMAGE_CATEGORY}_network_fsc_20avg.csv')
