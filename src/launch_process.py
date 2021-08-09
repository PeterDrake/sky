import os
from config import *

# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
os.system('SGE_Batch -r "' + EXPERIMENT_NAME + '_process" -c "python3 -u ../src/run_process.py"')
# os.system('SGE_Batch -r "' + EXPERIMENT_NAME + '_process" -q gpu.q -c "python3 -u ../src/run_process.py"')