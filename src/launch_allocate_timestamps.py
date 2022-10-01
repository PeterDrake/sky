import os

# TODO This has probably been supplanted with launch_allocate_timestamps.sh
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
os.system('SGE_Batch -r "dubious_allocation" -c "python3 -u ../src/run_allocate_timestamps.py shcu_dubious_data.csv dubious"')
os.system('SGE_Batch -r "typical_allocation" -c "python3 -u ../src/run_allocate_timestamps.py shcu_typical_data.csv typical"')
