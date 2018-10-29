# sky
<i>Applying convolutional neural networks to the task of semantic segmentation on (meteorological) clouds.</i>

<b>Setup</b>: 
- Download data from a Total Sky Imager (We use TSI C1 in the SGP) and unpack the tars into a convenient location.
- Look through the documentation in each file ending in launch.py. These will tell you about the parameters to set for your specific configuration
- Run the launch.py files in the order listed below. Before running a new file you should wait for the previous to finish.


<b>Programs to run (<i>Currently only on BLT</i>)</b>:
- preprocess_setup_launch.py: creates batches and sets many parameters used in preprocessing.
- preprocess_launch.py: launches parallel tasks to simplify batches of photos and decision images.
- preprocess_stamps_launch.py: separates data into training, validation, and testing, and makes final preparations for training.
- train_launch.py: defines parameters for training and launches the training process for several networks.
- process_launch.py: defines parameters for processing specific sky photos. Launches a number of jobs in parallel.
- fsc_launch.py: computes the fractional sky cover statistic for each decision image produced by the network and saves results in a csv file.

<b>To generate our plots: (<i>Currently not on BLT</i>)</b>
- fsc_analyze_launch: requires fsc_launch to be run on good and bad data. Compares network fsc statistic to the TSI and ARSCL.
- plot_learning_curve_launch.py: plots accuracy vs batch for the networks training process. Can be run after training is complete.


