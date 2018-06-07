import unittest
import os
from preprocess import *


class TestPreprocess(unittest.TestCase):
	INPUT_DIR = 'test_input'
	OUTPUT_DIR = 'test_output'
	TIMES = [20150208093000, 20171113141130, 20171113192200]

	@classmethod
	def setUpClass(cls):
		pass

	def tearDown(self):
		os.rmdir(self.OUTPUT_DIR)

	def test_creates_directories(self):
		create_dirs(self.OUTPUT_DIR, self.TIMES)
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simpleimage/2015/0208'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simpleimage/2017/1113'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simplemask/2015/0208'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simplemask/2017/1113'))
