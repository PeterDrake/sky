import unittest
import os
from shutil import rmtree
from preprocess import *


class TestPreprocess(unittest.TestCase):
	INPUT_DIR = 'test_input'
	OUTPUT_DIR = 'test_output'
	TIMES = [20150208093000, 20171113141130, 20171113192200]

	@classmethod
	def setUpClass(self):
		if os.path.isdir(self.OUTPUT_DIR):
			rmtree(self.OUTPUT_DIR)
		create_dirs(self.TIMES, self.OUTPUT_DIR)

	def test_creates_directories(self):
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simpleimage/2015/0208'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simpleimage/2017/1113'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simplemask/2015/0208'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simplemask/2017/1113'))

