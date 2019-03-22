"""
This file sets various parameters used in the experiment.
"""

# Variable used to run our code on BLT. To run locally set to False.
BLT = True

# Experiment label: used for organizing data. This should be a unique identifier like "e81-00" and should be changed
# with each run through the experiment.
EXPERIMENT_LABEL = "e84-00"

# Paths for typical (training & evaluation) and dubious (evaluation) data
TYPICAL_DATA_DIR = "typical_data"
TYPICAL_DATA_CSV = "typical_data/shcu_typical_data.csv"
DUBIOUS_DATA_DIR = "dubious_data"
DUBIOUS_DATA_CSV = "dubious_data/shcu_dubious_data.csv"

# When not set to None, this is the number of images to use from each dataset (typical and dubious). For a brief run
# through the experiment this can be set to something like 1000. When set to None, the experiment runs on all images
# specified in TYPICAL_DATA_CSV and DUBIOUS_DATA_CSV.
SMALL_PROCESS_SIZE = None

# Specify the structure of the network. This defines the number and ordering of layers as well as the type and size of
# each layer.
NETWORK_STRUCTURE = 'a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e g:conv-3-32-f h:concat-g-in i:conv-3-4-h'

# The number of sky/decision image pairs to train on in a single batch. We recommend setting this as high as possible
# during training. For our GTX 1080 ti the maximum number of images we can use in a batch is 23. On BLT, our CPU-cluster
# computer we can use upwards of 50 images.
TRAINING_BATCH_SIZE = 10

# This is the number of batches to run during training. We recommend setting this so that TRAINING_BATCH_SIZE multiplied
# by NUM_TRAINING_BATCHES is around 100,000. For a brief run through the experiment this can be made significantly
# smaller without too much performance loss.
NUM_TRAINING_BATCHES = 30

# This is the learning rate for training. We recommend setting this to a small value (1e-4 or smaller) with a large number
# of training batches. If you decrease the number of training batches significantly, consider increasing the learning rate.
LEARNING_RATE = 1e-4

# Set the maximum number of batches in a row allowed without progress. Setting this to None will effectively not bother
# with early stopping.
EARLY_STOPPING = 300

# Decide to keep track of the network with the highest validation accuracy. If set to True, then the final network will
# be the one with the highest observed validation accuracy.
TRACK_BEST_NETWORK = True

# =========================== Local Configurations (Ignore if BLT = True) =========================== #

# Path to directory downloaded from ARM. Must have the folders "CloudMask" and "SkyImage".
RAW_DATA_DIR = "D:\\Documents - Hard Drive\\Lewis & Clark\\Research\\Sky ML\\TSI_C1"

# Path to directory in which network data will be saved. Additionally, network-processed decision images will be
# saved to results/masks
RESULTS_DIR = "C:\\Users\\Maxwell\\PycharmProjects\\sky\\results"


# ====================== BLT - Specific Configurations (Ignore if BLT = False) ====================== #
if BLT:
	# Path to directory downloaded from ARM. Must have the folders "CloudMask" and "SkyImage".
	RAW_DATA_DIR = "/home/users/jkleiss/TSI_C1"

	# Path to directory in which network data will be saved. Additionally, network-processed decision images will be
	# saved to results/masks
	RESULTS_DIR = "results"

# The number of sky/decision image pairs to preprocess in a single job
PREPROCESS_BATCH_SIZE = 10000

# The number of networks to train simultaneously and the job's priority
NUM_NETWORKS = 1
JOB_PRIORITY = 25

# The number of processing tasks to launch for each of typical and dubious data (Per trained network)
NUM_PROCESS_BATCHES = 1
