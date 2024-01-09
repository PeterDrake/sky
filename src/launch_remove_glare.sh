#!/bin/bash
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
# We don't need to do this for dubious data, because we don't train on dubious data
#python3 -u ../src/run_remove_glare.py shcu_dubious_data.csv
python3 -u ../src/run_remove_glare.py shcu_typical_data.csv
