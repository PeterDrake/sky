"""
This file sets various parameters used in the experiment.
"""

# Variable used to run our code on BLT. To run locally set to False.
BLT = False

# Experiment label: used for organizing data. This should be a unique identifier like "e81-00" and should be changed
# with each run through the experiment.
EXPERIMENT_LABEL = "e84-00"

# Paths for typical (training & evaluation) and dubious (evaluation) data
TYPICAL_DATA_DIR = "typical_data"
TYPICAL_DATA_CSV = "typical_data/shcu_typical_data.csv"
DUBIOUS_DATA_DIR = "dubious_data"
DUBIOUS_DATA_CSV = "dubious_data/shcu_dubious_data.csv"

# Allows a small subset of typical and dubious data to be used (Used for debugging, or a quick run through the
# experiment. Set to 'None' to use the full set of available data.
SMALL_PROCESS_SIZE = 1000

# Specify the structure of the network. This defines the number and ordering of layers as well as the type and size of
# each layer.
NETWORK_STRUCTURE = 'a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-4-h'

# The number of sky/decision image pairs to train on in a single batch and the number of batches/steps to perform.
TRAINING_BATCH_SIZE = 10
NUM_TRAINING_BATCHES = 30

# Set the learning rate for training.
LEARNING_RATE = 0.01


# =========================== Local Configurations (Ignore if BLT = True) =========================== #

# Path to directory downloaded from ARM. Must have the folders "CloudMask" and "SkyImage".
RAW_DATA_DIR = "D:\\Documents - Hard Drive\\Lewis & Clark\\Research\\Sky ML\\TSI_C1"

# Path to directory in which network data will be saved
RESULTS_DIR = "C:\\Users\\Maxwell\\PycharmProjects\\sky\\results"


# ====================== BLT - Specific Configurations (Ignore if BLT = False) ====================== #
if BLT:
	# Path to directory downloaded from ARM. Must have the folders "CloudMask" and "SkyImage".
	RAW_DATA_DIR = "/home/users/jkleiss/TSI_C1"

	# Path to directory in which network data will be saved
	RESULTS_DIR = "results"

# The number of sky/decision image pairs to preprocess in a single job
PREPROCESS_BATCH_SIZE = 1500

# The number of networks to train simultaneously and the job's priority
NUM_NETWORKS = 1
JOB_PRIORITY = 25

# The number of processing tasks to launch for each of typical and dubious data (Per trained network)
NUM_PROCESS_BATCHES = 1


