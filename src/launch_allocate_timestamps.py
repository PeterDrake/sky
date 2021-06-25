import os

os.system('SGE_Batch -r "dubious_allocation" -c "python3 -u ../src/run_allocate_timestamps.py shcu_dubious_data.csv False"')
os.system('SGE_Batch -r "typical_allocation" -c "python3 -u ../src/run_allocate_timestamps.py shcu_typical_data.csv True"')
