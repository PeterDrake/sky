# Pipeline

We assume that all of the ARM data have been downloaded and untarred. We also assume we have the corresponding .csv
files (listing shallow cumulus timestamps). All of these are in locations outside of this directory.

Our pipeline involves the following steps.

## Preprocess the Data

1. Clean .csv files to verify that we have photos and TSI masks for all timestamps. Write these revised .csv files.
1. Create directories for all timestamps that are listed in the two .csv files.
1. In batches, preprocess each photo and TSI mask:
   1. The photo is centered, is cropped, and has a black border.
   1. The TSI mask has these same changes; also the sun is removed and each green pixel is replaced with the color of
   the nearest non-green pixel.
1. Subdivide timestamps into training, validation, and test sets.

## Train the Model

1. Set the experiment name and choice of network definition file in config.py. The training process won't allow
   the user to continue if the experiment name is already in results/experiment_log.csv or the code is not in a clean
   git state.
1. Build the network.
1. Train the network and save it in a directory for the current experiment (also updating the experiment log).

## Apply the Network

1. Run photos through our network to produce network masks.
1. Use network masks to create a .csv file of network FSCs.

## Produce Plots

1. Plot learning curve.
1. Analyze results (including producing plots for publication).

# Directory Structure

```
README.md
src (source code)
    *.py
doc (documentation)
    *.md
data (these are all generated and therefore *not* under version control)
    shcu_dubious_data.csv (our cleaned up version)
    shcu_typical_data.csv (our cleaned up version)
    typical_training_timestamps
    typical_validation_timestamps
    dubious_validation_timestamps
    typical_testing_timestamps
    dubious_testing_timestamps
    photos
        20120501 (and similar years/months/dates)
            20120501170430_photo.jpg (preprocessed)
    tsi_masks (structured like photos, but filenames end in _tsi_mask.png)
raw_csv
    readme_with_Jess_edits.pdf
    shcu_dubious_data.csv (raw version)
    shcu_typical_data.csv (raw version)
    TSI_data_explanation.pdf
results (these are all generated and therefore *not* under version control)
    experiment_log.csv (running an experiment adds a line to this file)
    exp00001 (results of experiment 00001)
        net.h5
        network_masks (structured like ../data/photos but filenames end in _network_mask.png)
        network_fsc.csv
    exp00002
    ...
    sandbox (similar to exp00001, but used for "junk" experiments that we don't care about saving)
test (test source code)
    *.py
test_data (analogous to data)
test_raw_csv (analogous to raw_csv)
    shcu_dubious_data.csv (simple test version in raw form)
    shcu_typical_data.csv (simple test version in raw form)
test_raw_data (analogous to external raw data directory, but much smaller)
    CloudMask
    SkyImage
test_results (analogous to results)
```