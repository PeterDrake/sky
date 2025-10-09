#!/bin/bash
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
export LD_LIBRARY_PATH="/usr/local/cuda-12.3/lib64:$LD_LIBRARY_PATH"
export PATH="/usr/local/cuda-12.3/bin:$PATH"
export CUDA_VISIBLE_DEVICES=$SLURM_STEP_GPUS
source ../.venv/bin/activate
python3 -u ../src/run_train.py
