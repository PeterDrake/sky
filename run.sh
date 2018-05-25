#!/bin/bash

echo $options
# The %% * is a perverse trick to get first word of options, which is the job name
SGE_Batch -r "${options%% *}" -c "python3 -u analyze.py $options" -P 1
