#!/bin/bash
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
python3 -u ../src/run_allocate_timestamps.py shcu_dubious_data.csv dubious
python3 -u ../src/run_allocate_timestamps.py shcu_typical_data.csv typical
