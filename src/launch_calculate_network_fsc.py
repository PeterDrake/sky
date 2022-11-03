import os

# TODO This has probably been supplanted with launch_calculate_network_fsc.sh
# NOTE: Run this from the `blt_job_output` directory, which should be at the same level as src.
os.system('SGE_Batch -r "network_fsc" -c "python3 -u ../src/run_calculate_network_fsc.py"')
