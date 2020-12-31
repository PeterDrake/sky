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

1. Build the network or load a pretrained one.
1. Train the network.

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
    training_timestamps
    validation_timestamps
    typical_testing_timestamps
    dubious_testing_timestamps
    photos
        2012 (and similar years)
            0501 (and similar month/dates)
                20120501170430_photo.jpg (preprocessed)
    tsi_masks (structured like photos)
    network_masks (structured like photos)
    network_fsc.csv
raw_csv
    readme_with_Jess_edits.pdf
    shcu_dubious_data.csv (raw version)
    shcu_typical_data.csv (raw version)
    TSI_data_explanation.pdf
test (test source code)
    *.py
test_raw_csv (analogous to raw_csv)
    shcu_dubious_data.csv (simple test version in raw form)
    shcu_typical_data.csv (simple test version in raw form)
test_raw_data (analogous to external raw data directory, but much smaller)
    CloudMask
    SkyImage
test_data (analogous to data)
```