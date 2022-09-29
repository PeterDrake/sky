#!/bin/bash
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
python3 -u ../src/run_preprocess shcu_dubious_data.csv
python3 -u ../src/run_preprocess shcu_typical_data.csv
