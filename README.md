# Sky Machine Learning

Applying convolutional neural networks to the task of semantic segmentation of (meteorological) clouds. 


## Quick Overview



## Getting Started

### Installing Dependencies

Dependencies used are <i>tensorflow, numpy, matplotlib, pandas, pickle, pillow (PIL), and scipy.</i> These will need to be installed prior to running our code.

### Running the Project on Your Machine

After downloading our code from our repository, open the configuration file (config.py) and set the desired parameters for your machine. Note that you will have to ensure that "BLT = False" for the code to run properly on your computer.

Once the configuration file is set up, you should be good to go. Now you just need to run the files ending in launch.py in the following order:
<ol>
  <li>preprocess_setup_launch.py</li>
  <li>preprocess_stamps_launch.py</li>
  <li>preprocess_launch.py</li>
  ...
</ol>

Note that this process takes about a week end-to-end on our cluster computer (BLT), so plan acccordingly if you intend to recreate our experiment. 

<b><i>If you do not intend to run our entire experiment on your computer, make sure you set <u>SMALL_PROCESS_SIZE</u> to a sufficiently small value (A few thousand should do) in config.py</i></b>.
