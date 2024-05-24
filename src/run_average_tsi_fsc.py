from FscAverager import FscAverager
from config import *
import sys

# TODO We're only doing validation now; eventually we'll need to do this for testing data
suffix = sys.argv[1]
avg = FscAverager(DATA_DIR, 'typical_validation_tsi_fsc.csv', half_width=10, min_stamps=4, interval=5)
avg.write_averages(f'typical_validation_tsi_fsc_20avg{suffix}.csv')
if suffix == '':  # Temporary, because we haven't de-glared dubious data yet
    avg = FscAverager(DATA_DIR, 'dubious_validation_tsi_fsc.csv', half_width=10, min_stamps=4, interval=5)
    avg.write_averages(f'dubious_validation_tsi_fsc_20avg{suffix}.csv')
