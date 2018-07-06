#!/bin/bash

SGE_Batch -r "analysis_$1" -c "python3 -u analyze.py $1" -P 1
