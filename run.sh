#!/bin/bash

echo $options
# The %% * is a perverse trick to get first word of options, which is the job name
#echo "${options%% *}"
#echo "python3 -u preprocess.py $options"
SGE_Batch -r "${options%% *}" -c "python3 -u preprocess.py $options" -P 1
