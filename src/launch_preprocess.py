import os

# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
os.system('SGE_Batch -r "dubious_preprocessing" -c "python3 -u ../src/run_preprocess.py shcu_dubious_data.csv"')
os.system('SGE_Batch -r "typical_preprocessing" -c "python3 -u ../src/run_preprocess.py shcu_typical_data.csv"')
