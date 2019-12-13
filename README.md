# Sky Machine Learning

Applying convolutional neural networks to the task of semantic segmentation of (meteorological) clouds. 


## Quick Overview

## Getting Started

### Setting up your Environment

If you have successfully run python scripts on your machine in the past and you are comfortable with your current editor, you may skip this step. 

We recommend downloading and installing <a href="https://git-scm.com/downloads">git</a>, a version control system that integrates well with github. This will help you download our code and stay up-to-date with bug fixes and other changes. We recommend installing git with the default installation settings if possible. 

If you don't have python installed on your system, you will need to download and install python on your system. You can get python <a href="https://www.python.org/downloads/">here</a>. If you're on Windows, we recommend including Python in your PATH when using the setup wizard.

Once you have python installed on your system, you will need an integrated development environment (IDE) to make a few code changes specific to your system. We recommend using <a href="https://www.jetbrains.com/pycharm/download/">PyCharm</a> because it has many useful features, is well-documented, and seemlessly integrates with git. 

Whatever environment you decide to use, you will need have the following packages installed prior to running our code: <i>tensorflow, numpy, matplotlib, pandas, pickle, pillow (PIL), and scipy.</i>


### Downloading the data
Our data consists of sky images and and cloud masks from 5/1/2012 to 9/24/2017. The data belongs to <a href="https://www.arm.gov/">https://www.arm.gov/</a>, so to obtain it for yourself you will need to follow the following steps:
<ol>
  <li>Log in or create an account with ARM</li>
  <li>Go to the <a href="https://www.archive.arm.gov/discovery/#v/results/s/fsite::sgp.P/ffac::sgp.C1/fdpl::sgptsicldmaskC1.a1/fdpl::sgptsiskyimageC1.a1">Data Discovery</a> page and select the checkboxes next to "tsicldmask C1" and "tsiskyimage" </li>
  <li>Proceed to checkout with the data and download as tarred files.</li>
  <li>Untar the downloaded files into folders named "CloudMask" and "SkyImage"</li>
</ol>

It can take several days for ARM to stage the files for download and the files are several gigabytes altogether. Once your data in downloaded and unpacked into a convenient location, you're all set.

### Running the Project on Your Machine

After downloading our code from our repository, open the configuration file (config.py) and set the desired parameters and file paths for your machine. Note that you will have to ensure that "BLT = False" for the code to run properly on your computer.

Navigate to the file path you have specified in the config file as RAW_DATA_DIR. Then create two new directories named SkyImage and CloudMask and put the skyimage and cldmask tar files in their respective directories. Once the files are organized, running unpack_tars.py will unpack all of the tarred files into their appropriate subdirectories in CloudMask and SkyImage.

Once the configuration file is set up, you should be good to go. Now you just need to run the files ending in launch.py in the following order:
<ol>
  <li> <strong>preprocess_setup_launch.py</strong></li>
  <li><strong>preprocess_stamps_launch.py</strong></li>
  <li><strong>center_preprocess_launch.py</strong></li>
  <li><strong>train_model_1_launch.py</strong></li>
  <li><strong>plot_learning_curve_keras.py</strong></li>
  <li><strong>make_decision_images.py</strong></li>
  <li><strong>fsc_launch.py</strong></li>
  <li><strong>fsc_analyze_launch.py</strong></li> 
</ol>

Note that you can change various training-specific parameters in config.py and run train_launch.py several times without needing to run the preprocessesing tasks again. For example - once the preprocessing tasks are done and you've trained the network once, you may wish to try out a different learning rate or train for a different number of batches. You can do this simply by modifying EXPERIMENT_LABEL in config.py so that your existing network is not overwritten, and then change LEARNING_RATE and NUM_TRAINING_BATCHES to your desired values. Once these changes have been made, running train_launch.py will begin training a new network with your new configurations.
