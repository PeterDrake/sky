#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finds the zenith area of TSI skymasks
"""

import os
import sys

from fsc_launch import get_fsc_from_file
from process_launch import get_network_mask
from utils import extract_data_from_csv

# DONE: Make sure fsc is easily computed from simplified masks
# DONE: Grab fsc info from shcu_good_data csv file (and possibly other files in the future)
# DONE?: Read in some new masks from our network in good_data
# TODO: Loosely compare between the different methods. The csv info should agree with the simplified masks,
# TODO: hopefully the network outputs as well.
# TODO: Be able to display simple masks and network output for images with the most disagreement


if __name__ == '__main__':
	print(134)
	exp_label = sys.argv[1]  # The experiment number / directory name in results
	times = sorted(list(extract_data_from_csv('shcu_good_data.csv', 'timestamp_utc')))
	with open('results/' + exp_label + '/' + 'fsc.csv', 'w') as f:
		f.write('timestamp_utc, fsc_z, fsc_thn_z, fsc_opq_z')
		for t in times:
			if not os.path.isfile(get_network_mask(t, exp_label)):
				continue
			fsc_z, fsc_thn_z, fsc_opq_z = get_fsc_from_file(get_network_mask(t, exp_label))
			f.write('{}, {}, {}. {}'.format(t, fsc_z, fsc_thn_z, fsc_opq_z))
