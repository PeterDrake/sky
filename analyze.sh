#!/bin/bash

for i in {0..4}
do
    SGE_Batch -r "analysis_$i" -c "python3 -u analyze.py $1$i" -P 1
done