#!/bin/bash
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
# TODO Add --gres=gpu:4 to use GPUs
python3 -u ../src/run_train.py
