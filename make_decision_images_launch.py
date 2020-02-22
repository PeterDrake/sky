import os
from config import *
# from make_decision_images import process


def launch_process(job_name, input_dir, input_file_path):
	"""Starts processing tasks."""

	name = job_name + EXPERIMENT_LABEL

	if BLT:
		os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u make_decision_images.py {} {}" -P 1'.format(name, input_dir, input_file_path))
	else:
		print("ERROR: CODE NOT WRITTEN YET. BLT = TRUE")	#TODO make this into a functioning statment that runs process.py on local machine	

if __name__ == "__main__":

	launch_process("process-train-stamps", TYPICAL_DATA_DIR, "/train.stamps")
	launch_process("process-valid-stamps", TYPICAL_DATA_DIR, "/valid.stamps")
	launch_process("process-poster-test", DUBIOUS_DATA_DIR , "/poster_test.stamps")
	