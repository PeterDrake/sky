from FscAverager import FscAverager
from config import *

# TODO We're only doing validation now; eventually we'll need to do this for testing data
avg = FscAverager(DATA_DIR, 'typical_validation_tsi_fsc.csv', half_width=10, min_stamps=4, interval=5)
avg.write_averages('typical_validation_tsi_fsc_20avg.csv')
avg = FscAverager(DATA_DIR, 'dubious_validation_tsi_fsc.csv', half_width=10, min_stamps=4, interval=5)
avg.write_averages('dubious_validation_tsi_fsc_20avg.csv')
