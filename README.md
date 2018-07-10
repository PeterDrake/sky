# sky
Applying machine learning to the task of segmentation on (meteorological) clouds.


To setup: 
- download data from a Total Sky Imager (We use TSI C1 in the SGP) and unpack the tars into a convenient location.
- look through the documentation in each file ending in launch.py. These will tell you about the parameters to set for your specific configuration
- run the launch.py files in the order listed below. Before running a new file you should wait for the previous to finish.


Programs to run (Currently only on BLT):

preprocess_setup_launch.py -- creates batches and sets many parameters used in preprocessing.

preprocess_launch.py -- launches parallel tasks to simplify batches of photos and decision images.

preprocess_stamps_launch.py -- separates data into training, validation, and testing, and makes final preparations for training.

train_launch.py -- defines parameters for training and launches the training process for several networks.

process_launch.py -- defines parameters for processing specific sky photos. Launches a number of jobs in parallel.

fsc_launch.py -- computes the fractional sky cover statistic

fsc_analyze_launch -- requires fsc_launch to be run on good and bad data. Compares network fsc statistic to the TSI and ARSCL.

plot_learning_curve_launch.py -- plots accuracy vs batch for the networks training process. Can be run after training is complete.


Other programs:

show_output.py shows the network's output for a particular image

show_kernels.py shows the kernels in the first convolutional layer

analyze.py finds the images for which the network does worst and displays how they disagree with the targets
