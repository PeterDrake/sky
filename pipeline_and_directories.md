# Pipeline

We assume that all of the ARM data have been downloaded and untarred. We also assume we have the corresponding .csv
files (listing shallow cumulus timestamps) is in each directory.

Our pipeline involves the following steps.

## Preprocess the Data

1. Clean .csv files to verify that we have photos and TSI masks for all timestamps. Write these revised .csv files into
   directories typical_data and dubious_data.
1. Subdivide timestamps into training, validation, and test sets.
1. Create directories for all timestamps that are listed in the two .csv files.
1. In batches, preprocess each photo and TSI mask:
   1. The photo is centered, is cropped, and has a black border.
   1. The TSI mask has these same changes; also the sun is removed and any green pixels are replaced with the average
      of surrounding pixels.

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
typical_data
    shcu_typical_data.csv (our cleaned up version)
    training_timestamps
    validation_timestamps
    testing_timestamps
    photos
        2012 (and similar years)
            0501 (and similar month/dates)
                20120501170430_photo.jpg (preprocessed)
    tsi_masks (structured like photos)
    network_masks (structured like photos)
    network_fsc.csv
dubious_data
    shcu_dubious_data.csv (our cleaned up version)
    testing_timestamps
    photos
        2012 (and similar years)
            0501 (and similar month/dates)
                20120501170430_tsi_mask.png (preprocessed)
    tsi_masks (structured like photos)
    network_masks (structured like photos)
    network_fsc.csv
```