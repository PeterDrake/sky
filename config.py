"""
	This file defines many parameters used in the experiment. The configuration file is broken down into three main
	sections: User-Defined Configurations, Training/Experiment Parameters, and BLT - Specific Configurations.

	Normal users should only need to modify the User-Defined Configurations section in order to run our experiment. Here
	users will want to change RAW_DATA_DIR to match the path to the directory containing their unpacked/untarred data
	from ARM (link in README). Because preprocessed and processed data can still be quite large (Several Gigabytes), we
	offer the user an opportunity to change the TYPICAL_DATA, DUBIOUS_DATA, and RESULTS_DIR directories to different
	locations.

	Experienced users may wish to change the Training/Experiment Configurations in order to modify the training process.
	This is not recommended for recreating our experiment. Users who do modify these configurations should do so with
	care and read the available documentation before making changes.

	The BLT - Specific Configurations section defines parameters that are used on BLT (a cluster computer hosted by
	Lewis & Clark College's Watzek Digital Initiatives team). Documentation: https://watzek.github.io/LC-BLT/
	This section should only be modified by researchers working on this project.

	Note: Users who want to run the full experiment on their computer can do so with minimal effort by changing which
	lines are commented out in the training/experiment configurations section. Users wishing to do a full run through
	of the experiment should look to the following variables: SMALL_PROCESS_SIZE, TRAINING_BATCH_SIZE, and
	NUM_TRAINING_BATCHES.

"""

# ==================================================================================================================== #
#                                                                                                                      #
#                                               User-Defined Configurations                                            #
#                                                                                                                      #
# ==================================================================================================================== #

# Path to directory downloaded from ARM. Must have the folders "CloudMask" and "SkyImage", and must be unpacked/untarred
# prior to running any part of our project. See the README for more detailed instructions.
RAW_DATA_DIR = "D:\\Documents - Hard Drive\\Lewis & Clark\\Research\\Sky ML\\TSI_C1"

# Paths for typical (training & evaluation) and dubious (evaluation) data. These directories need not exist prior to
# running the experiment from scratch; the preprocessing scripts will create and populate these directories with
# simplified sky and decision images from the RAW_DATA_DIR.
TYPICAL_DATA_DIR = "typical_data"
DUBIOUS_DATA_DIR = "dubious_data"

# Path to directory in which network data will be saved. Additionally, network-processed decision images will be
# saved to results/masks.
RESULTS_DIR = "results"

# ==================================================================================================================== #
#                                                                                                                      #
#                                            Training/Experiment Configurations                                        #
#                                                                                                                      #
# ==================================================================================================================== #


# Variable used to run our code on BLT. To run locally set to False.
BLT = True

# Variable to indicate which network architecture (model) to use.
MODEL_TYPE = "model_4"

# Variable to only use validation data for computing fsc (Saves a lot of time if just making plots with validation data,
# but you'll want to set this to false if you are planning on making plots that involve other data)
USE_VALID_FSC = True

# A unique identifier for the network being trained/in use. This can be something like "e2019-001". If testing out several
# networks, be sure to change this with each run. The training process WILL overwrite any existing saved networks
# identified by this experiment label.
EXPERIMENT_LABEL = "e2019-003"

# Paths to csv files for typical and dubious data.
TYPICAL_DATA_CSV = "typical_data/shcu_typical_data.csv"
DUBIOUS_DATA_CSV = "dubious_data/shcu_dubious_data.csv"

# Paths to timestamps for typical and dubious data.
TYPICAL_VALID_FILE = TYPICAL_DATA_DIR + "/valid.stamps"
DUBIOUS_VALID_FILE = DUBIOUS_DATA_DIR + "/poster_valid.stamps"

# The number of sky/decision image pairs to preprocess in a single job. When running locally, set this to 200,000. There
# is no benefit to creating multiple batches for preprocessing data when not on BLT as our code does not run preprocess
# tasks in parallel. If BLT is set to True, this is set to 10000 -- our preprocess code runs in parallel on BLT.
PREPROCESS_BATCH_SIZE = 200000

# When not set to None, this is the number of images to use from each dataset (typical and dubious). For a brief run
# through the experiment this can be set to something like 1000. When set to None, the experiment runs on all images
# specified in TYPICAL_DATA_CSV and DUBIOUS_DATA_CSV.
SMALL_PROCESS_SIZE = None  # Full Run
# SMALL_PROCESS_SIZE = 1000  # Small run

# The number of sky/decision image pairs to train on in a single batch. We recommend setting this as high as possible
# during training. For our GTX 1080 ti the maximum number of images we can use in a batch is 23.
TRAINING_BATCH_SIZE = 16  # For a run with a GTX 1080 Ti
# TRAINING_BATCH_SIZE = 10  # Small run

# This is the number of batches to run during training. We recommend setting this so that TRAINING_BATCH_SIZE multiplied
# by NUM_TRAINING_BATCHES is around 100,000. For a brief run through the experiment this can be made significantly
# smaller without too much performance loss.
NUM_TRAINING_BATCHES = 5000  # Full run (with a graphics card)
# NUM_TRAINING_BATCHES = 2000  # Medium run (Training takes a long time without a graphics card)
# NUM_TRAINING_BATCHES = 30  # Small run

# This is the learning rate for training. We recommend setting this to a small value (1e-4 or smaller) with a large
# number of training batches. If you decrease the number of training batches significantly, consider increasing the
# learning rate.
LEARNING_RATE = 1e-4

# Set the maximum number of batches in a row allowed without progress. Setting this to None will effectively not bother
# with early stopping.
EARLY_STOPPING = 300

# Decide to keep track of the network with the highest validation accuracy. If set to True, then the final network will
# be the one with the highest observed validation accuracy.
TRACK_BEST_NETWORK = True

# Specify the structure of the network. This defines the number and ordering of layers as well as the type and size of
# each layer.
NETWORK_STRUCTURE = 'a:conv-3-32-in b:maxpool-1-100-a c:maxpool-100-1-a d:concat-a-b e:concat-c-d f:conv-3-32-e ' \
					'g:conv-3-32-f h:concat-g-in i:conv-3-4-h'

# ==================================================================================================================== #
#                                                                                                                      #
#                                            BLT - Specific Configurations                                             #
#                                                                                                                      #
# ==================================================================================================================== #


if BLT:
	# Path to directory downloaded from ARM. Must have the folders "CloudMask" and "SkyImage".
	RAW_DATA_DIR = "/home/users/jkleiss/TSI_C1"

	# Path to directory in which network data will be saved. Additionally, network-processed decision images will be
	# saved to results/masks
	RESULTS_DIR = "results"

	# TRAINING_BATCH_SIZE = 50  # Largest batch size possible

	PREPROCESS_BATCH_SIZE = 10000

# The number of networks to train simultaneously and the job's priority
NUM_NETWORKS = 1
JOB_PRIORITY = 5

# The number of processing tasks to launch for each of typical and dubious data (Per trained network)
NUM_PROCESS_BATCHES = 1
