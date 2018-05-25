#!/bin/bash

for i in {0..5}
do
    #SGE_Batch -r "analysis_$i" -c "python3 -u analyze.py $1" -P 1
    echo "stuff_$i"
done