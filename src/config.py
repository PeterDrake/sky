# Directories on BLT used by various run_*.py programs
RAW_DATA_DIR = '/home/users/jkleiss/TSI_C1'
RAW_CSV_DIR = '../raw_csv'
DATA_DIR = '../data'

# Parameters for dividing timestamps into training, validation, and testing
TYPICAL_PROPORTIONS = [0.6, 0.2, 0.2]
TYPICAL_TIMESTAMP_FILENAMES = ['typical_' + c + '_timestamps' for c in ['training', 'validation', 'testing']]
DUBIOUS_PROPORTIONS = [0.5, 0.5]
DUBIOUS_TIMESTAMP_FILENAMES = ['dubious_' + c + '_timestamps' for c in ['validation', 'testing']]
