import os
from config import *

# TODO This has probably been supplanted with launch_process.sh
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
os.system('SGE_Batch -r "' + EXPERIMENT_NAME + '_process" -c "python3 -u ../src/run_process.py"')

# TODO Modify run_process to take these command-line arguments, then uncomment this (to parallelize processing)
# n = 21965  # Number of validation images
# for i in range(0, n, 3200):
#     j = min(i + 3200, n)
#     os.system('SGE_Batch -r "{}_process" -c "python3 -u ../src/run_process.py {} {}"'.format(EXPERIMENT_NAME, i, j))
