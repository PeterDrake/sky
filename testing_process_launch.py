"""
This program can be called after the train_launch.py finishes its task.

This program processes simplified sky images through the trained network to create decision images. Processing is run in
parallel if BLT is set to True, significantly reducing the time needed to process large numbers of sky images. If BLT is
set to False in the config file then processing is sequential.
"""

import os
from config import *
from process import process


def launch_process(input_data_csv, job_name, input_dir):
    """Starts processing tasks."""
    
    total_length = -1  # This file has a header
    for _ in open(input_data_csv):
        total_length += 1
    batch_length = int(total_length / NUM_PROCESS_BATCHES)
    for i in range(NUM_PROCESS_BATCHES):
        name = job_name + EXPERIMENT_LABEL + '-{:0>2}'.format(i)
        start = batch_length * i
        finish = batch_length * (i + 1) if batch_length * (i + 1) < total_length else total_length
        if BLT:
            os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u testing_process.py {} {} {} {}" -P 1'.format(name,
                                                                                                      int(start),
                                                                                                      int(finish),
                                                                                                      input_dir,
                                                                                                      input_data_csv))
        else:
            process(int(start), int(finish), input_dir, input_data_csv)


if __name__ == "__main__":
    launch_process(DUBIOUS_DATA_CSV, "process-dubious-", DUBIOUS_DATA_DIR)
    launch_process(TYPICAL_DATA_CSV, "process-typical-", TYPICAL_DATA_DIR)
