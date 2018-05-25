#!/bin/bash

SGE_Batch -r "analysis" -c "python3 -u analyze.py $1" -P 1
