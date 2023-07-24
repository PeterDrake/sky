# Directories used by various run_*.py programs
RAW_DATA_DIR = '/home/users/jkleiss/TSI_C1'
RAW_CSV_DIR = '../raw_csv'
DATA_DIR = '/home/drake/sky/data'
RESULTS_DIR = '/home/drake/sky/results'

# Parameters for dividing timestamps into training, validation, and testing
TYPICAL_PROPORTIONS = [0.6, 0.2, 0.2]
# TODO Do these really need to be lists?
TYPICAL_TIMESTAMP_FILENAMES = ['typical_' + c + '_timestamps' for c in ['training', 'validation', 'testing']]
DUBIOUS_PROPORTIONS = [0.5, 0.5]
DUBIOUS_TIMESTAMP_FILENAMES = ['dubious_' + c + '_timestamps' for c in ['validation', 'testing']]

# Current experiment name (e.g., 'exp00001'), or 'sandbox'
EXPERIMENT_NAME = 'su23_0003'

# Name (minus .py) of file containing network architecture
NETWORK_ARCHITECTURE = 'net_c64'

# Number of epochs to train for
TRAIN_EPOCHS = 20
