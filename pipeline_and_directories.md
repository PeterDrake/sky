# Pipeline

We assume that all of the ARM data have been downloaded and untarred. We also assume we have the corresponding .csv
files (listing shallow cumulus timestamps). All of these are in locations outside of this directory.

Our pipeline involves the following steps.

## Preprocess the Data

### What You Do

On BLT (from the `blt_job_output` directory), wait for each of the following steps to finish before doing the next one.

```
source /home/labs/drake/tensorflow_gpu_11.7/bin/activate
sbatch ../src/launch_preprocess.sh
```

```
sbatch ../src/launch_allocate_timestamps.sh
```

```
sbatch ../src/launch_calculate_tsi_fsc.sh
```

```
sbatch ../src/launch_remove_glare.sh

```

```
sbatch ../src/launch_average_tsi_fsc.sh
```

````
sbatch ../src/launch_collate_tsi_fsc_cf.sh
````

On a machine other than BLT (from the `src` directory):

```
python3 -u run_preprocess.py shcu_dubious_data.csv
python3 -u run_preprocess.py shcu_typical_data.csv
python3 -u run_allocate_timestamps.py shcu_dubious_data.csv dubious
python3 -u run_allocate_timestamps.py shcu_typical_data.csv typical
python3 -u run_calculate_tsi_fsc.py
python3 -u run_remove_glare.py
python3 -u run_average_tsi_fsc.py
python3 -u run_collate_tsi_fsc_cf.py
```

### What This Accomplishes

1. Clean .csv files to verify that we have photos and TSI masks for all timestamps. Write these revised .csv files.
2. Create directories for all timestamps that are listed in the two .csv files.
3. Preprocess each photo and TSI mask:
   1. The photo is centered, is cropped, and has a black border.
   1. The TSI mask has these same changes; also the sun is removed and each green pixel is replaced with the color of
   the nearest non-green pixel.
4. Subdivide timestamps into training, validation, and test sets.
5. Count opaque, thin, and clear pixels for each TSI mask.
6. Compute 15-minute averages of fractional sky cover.
7. Collate these with ceilometer cloud fractions.

## Train the Model

### What You Do

1. Set the experiment name in `config.py`. The training process won't allow
   the user to continue if the experiment name is already in `results/experiment_log.csv` or the code is not in a
   clean git state.
1. Set the network architecture name in `config.py`. The corresponding .py file in `src/model_architectures` gives the
   definition of the network architecture.
1. Build and train the network as described below.

On BLT, (from the `blt_job_output` directory):

```
source /home/labs/drake/tensorflow_gpu_11.7/bin/activate
sbatch --gres=gpu:4 ../src/launch_train.sh
```

(You don't need the first line, which activates the virtual environment, if it is already active.)

On a machine other than BLT (from the 'src' directory):

```
python3 -u run_train.py
```

### What This Accomplishes

1. Sets the experiment name and network architecture.
1. Build and train the network. The result is saved in a directory for the current experiment (also updating the
   experiment log).

## Process Images Using the Network

### What You Do

On BLT, (from the `blt_job_output` directory):

```
source /home/labs/drake/tensorflow_gpu_11.7/bin/activate
sbatch --gres=gpu:4 ../src/launch_process.sh
```

(You don't need the first line, which activates the virtual environment, if it is already active.)

On a machine other than BLT (from the 'src' directory):

```
python3 -u run_process.py
```

### What this Accomplishes

Run photos through our network to produce and save network masks.
   
## Compute Fractional Sky Coverage of Network Masks

### What You Do

On BLT, (from the `blt_job_output` directory), wait for each of the following steps to finish before doing the next one:

```
source /home/labs/drake/tensorflow_gpu_11.7/bin/activate
sbatch ../src/launch_calculate_network_fsc.sh
```

````
sbatch ../src/launch_average_network_fsc.sh
````

````
sbatch ../src/launch_collate_network_fsc_cf.sh
````

(You don't need the first line, which activates the virtual environment, if it is already active.)

On a machine other than BLT (from the 'src' directory):

```
python3 -u run_calculate_network_fsc.py
python3 -u run_average_network_fsc.py
python3 -u run_collate_network_fsc_cf.py
```

### What This Accomplishes

Use network masks to create .csv files of network FSCs.

## Produce Plots

### What You Do

1. Edit `src/config.py` to set EXPERIMENT_NAME to the experiment in which you're interested.
1. Run `grab_and_display_results.py`.

This is mainly for out internal use; it pulls down files from BLT
and produces various plots and other files in a directory (named for the timestamp) within `data_for_plotting`.

### What This Accomplishes
Downloads (from BLT) various files for the current experiment and then saves into a subdirectory of `data_for_plotting`:

1. Those files
2. rmse.txt, giving the RMSE values for fsc vs cf
3. stamps.txt, giving some 'interesting' timestamps
4. A triptych for each of these timestamps
5. The scatter plots of fsc vs cf
6. The learning curve

# Directory Structure

```
README.md
blt_job_output (output and error logs generated by BLT; not under version control)
.env (credentials for sftp and whatnot; not underversion control)
src (source code)
    model_architectures
        *.py (files describing various network architectures)
    *.py
    *.sh (shell scripts for running on BLT)
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
    dubious_validation_tsi_fsc.csv
    typical_validation_tsi_fsc.csv
    photos
        20120501 (and similar years/months/dates)
            20120501170430_photo.jpg (preprocessed)
    tsi_masks (structured like photos, but filenames end in _tsi_mask.png)
    tsi_masks_no_glare (just like tsi_masks, but with clouds removed from masks likely to contain glare, as defined by
      GlareRemove.py)
raw_csv
    readme_with_Jess_edits.pdf
    shcu_dubious_data.csv (raw version)
    shcu_typical_data.csv (raw version)
    TSI_data_explanation.pdf
results (these are all generated and therefore *not* under version control)
    experiment_log.csv (running an experiment adds a line to this file)
    exp00001 (results of experiment 00001)
        network.h5
        network_masks (structured like ../data/photos but filenames end in _network_mask.png)
        dubious_validation_network_fsc.csv
        typical_validation_network_fsc.csv
        training_history (for producing learning curves)
    exp00002
    ...
    sandbox (similar to exp00001, but used for "junk" experiments that we don't care about saving)
test (test source code)
    *.py
test_data (analogous to data)
test_network_masks (analogous to results/test_experiment/network_masks; this is in repository for computing FSC without generating masks)
test_raw_csv (analogous to raw_csv)
    shcu_dubious_data.csv (simple test version in raw form)
    shcu_typical_data.csv (simple test version in raw form)
test_raw_data (analogous to external raw data directory, but much smaller)
    CloudMask
    SkyImage
test_results (analogous to results)
test_network_masks (some network masks we can use to test FSC calculation; structuresd like results/exp00001/network_masks)
```