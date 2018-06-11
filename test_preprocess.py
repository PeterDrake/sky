import unittest
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

	def test_find_unpaired_images(self):
		actual = {'20131118133000', '20131118133030', '20131118133100', '20131118133130', '20131118133200',
		          '20131118133930'}
		self.assertEqual(actual, find_unpaired_images(self.INPUT_DIR, extract_all_times(self.INPUT_DIR)))

	def test_color_counts(self):
		img = np.array([[BLACK, BLUE, BLACK],
		                [WHITE, BLACK, WHITE]])
		probs = count_colors(img)
		correct = np.array([2, 1, 0, 3, 0])
		self.assertTrue((probs == correct).all())

	def test_remove_white_sun(self):
		img = np.array([[BLACK, BLUE, BLACK, BLACK, BLACK, BLACK, BLACK],
		                [BLACK, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK],
		                [BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, BLACK],
		                [BLACK, BLUE, BLACK, WHITE, WHITE, BLACK, BLACK],
		                [BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, BLACK],
		                [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
		                [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]])
		correct = np.array([[BLACK, BLUE, BLACK, BLACK, BLACK, BLACK, BLACK],
		                    [BLACK, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK],
		                    [BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, BLACK],
		                    [BLACK, BLUE, BLACK, BLACK, BLACK, BLACK, BLACK],
		                    [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
		                    [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
		                    [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]])
		# correct = (2,2)
		out = remove_white_sun(img, stride=1)
		self.assertTrue((out == correct).all())

	def test_find_image_path(self):
		self.assertEqual('test_input/simpleimage/2013/1118/', img_save_path(20131118133130, self.INPUT_DIR))

	def test_find_mask_path(self):
		self.assertEqual('test_input/simplemask/2013/1118/', mask_save_path(20131118133130, self.INPUT_DIR))
