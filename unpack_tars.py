"""
	This file is intended to be used to unpack the tars downloaded from arm.gov (See README for more details on how to
	download the data).

	Note: Before running this file, the user should ensure that they have defined RAW_DATA_DIR in config.py and that
	RAW_DATA_DIR contains directories SkyImage and CloudMask, each of which contain the skyimage and cloudmask tar files
	respectively.
"""

import glob
import tarfile
import os
from config import RAW_DATA_DIR

back = os.getcwd()
os.chdir(RAW_DATA_DIR)

files = glob.glob("SkyImage/*.jpg.tar")
for file in files:
	path = file[:-8]
	os.makedirs(path, exist_ok=True)
	tar = tarfile.open(file)
	tar.extractall(path=path)

files = glob.glob("CloudMask/*.png.tar")
for file in files:
	path = file[:-8]
	os.makedirs(path)
	tar = tarfile.open(file)
	tar.extractall(path=path)

os.chdir(back)
