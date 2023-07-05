from FscAverager import FscAverager
from config import *

# TODO We're only doing validation now; eventually we'll need to do this for testing data
avg = FscAverager(RESULTS_DIR + '/' + EXPERIMENT_NAME, 'typical_validation_network_fsc.csv')
avg.write_averages('typical_validation_network_fsc_15avg.csv')
avg = FscAverager(RESULTS_DIR + '/' + EXPERIMENT_NAME, 'dubious_validation_network_fsc.csv')
avg.write_averages('dubious_validation_network_fsc_15avg.csv')
