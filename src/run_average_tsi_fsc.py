from FscAverager import FscAverager
from config import *

# TODO We're only doing validation now; eventually we'll need to do this for testing data
avg = FscAverager(DATA_DIR, 'typical_validation_tsi_fsc.csv')
avg.write_averages('typical_validation_tsi_fsc_15avg.csv')
avg = FscAverager(DATA_DIR, 'dubious_validation_tsi_fsc.csv')
avg.write_averages('dubious_validation_tsi_fsc_15avg.csv')
