import os

os.system('SGE_Batch -r "dubious" -c "python3 -u run_preprocess.py shcu_dubious_data.csv"')
os.system('SGE_Batch -r "typical" -c "python3 -u run_preprocess.py shcu_typical_data.csv"')
