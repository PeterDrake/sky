import os
from config import *
from make_decision_images import process


def launch_process(input_data_csv, job_name, input_dir):
	"""Starts processing tasks."""

	name = job_name + EXPERIMENT_LABEL + '-{:0>2}'.format(i)

	if BLT:
		os.system('SGE_Batch -q gpu.q -r "{}" -c "python3 -u make_decision_images.py {} {}" -P 1'.format(name, input_dir, input_data_csv))
	else:
		print("")		

if __name__ == "__main__":

	custom = {'DecidePixelColors': DecidePixelColors}
	model = tf._api.v1.keras.models.load_model('model_1_23.h5', custom_objects=custom)

	launch_process(DUBIOUS_DATA_CSV, "process-dubious-", DUBIOUS_DATA_DIR)
	launch_process(TYPICAL_DATA_CSV, "process-typical-", TYPICAL_DATA_DIR)