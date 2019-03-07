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

### Running the Project on Your Machine

After downloading our code from our repository, open the configuration file (config.py) and set the desired parameters and file paths for your machine. Note that you will have to ensure that "BLT = False" for the code to run properly on your computer.

<b><em>If you do not intend to run our entire experiment on your computer, make sure <u>SMALL_PROCESS_SIZE</u> is set to a sufficiently small value (A few hundred or thousand should do) in config.py. For example:</em></b>
```
SMALL_PROCESS_SIZE = 300
```

If you <em>do</em> intend to run our entire experiment, set
```
SMALL_PROCESS_SIZE = None
```

and be aware that this process takes about a week end-to-end on our cpu-cluster computer (BLT). 

Once the configuration file is set up, you should be good to go. Now you just need to run the files ending in launch.py in the following order:
<ol>
  <li> <strong>preprocess_setup_launch.py</strong> - preprocesses TSI data.</li>
  <li><strong>preprocess_stamps_launch.py</strong></li>
  <li><strong>preprocess_launch.py</strong></li>
  <li><strong>train_launch.py</strong></li>
  <li><strong>process_launch.py</strong></li>
  <li><strong>fsc_launch.py</strong></li>
  <li><strong>fsc_analyze_launch.py</strong></li> 
  <li><strong>plot_learning_curve_launch.py</strong></li>
</ol>

