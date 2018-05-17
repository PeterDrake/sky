#!/bin/bash

echo $options
SGE_Batch -r "${options[0]}" -c "python3 -u preprocess.py $@options" -P 1
