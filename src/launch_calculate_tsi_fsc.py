import os

# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
os.system('SGE_Batch -r "tsi_fsc" -c "python3 -u ../src/run_calculate_tsi_fsc.py"')