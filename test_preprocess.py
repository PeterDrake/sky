import unittest
from shutil import rmtree

from preprocess_setup_launch import *


class TestPreprocess(unittest.TestCase):
	INPUT_DIR = 'test_input'
	OUTPUT_DIR = 'test_output'

	@classmethod
	def setUpClass(self):
		if os.path.isdir(self.OUTPUT_DIR):
			rmtree(self.OUTPUT_DIR)
		TIMES = [20150208093000, 20171113141130, 20171113192200]
		create_dirs(TIMES, self.OUTPUT_DIR)

	def test_creates_directories(self):
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simpleimage/2015/0208'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simpleimage/2017/1113'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simplemask/2015/0208'))
		self.assertTrue(os.path.isdir(self.OUTPUT_DIR + '/simplemask/2017/1113'))

	def test_find_unpaired_images(self):
		actual = {'20131118133000', '20131118133030', '20131118133100', '20131118133130', '20131118133200',
			'20131118133930'}
		self.assertEqual(actual,
				find_unpaired_images(extract_all_times(self.INPUT_DIR, ['/SkyImage', '/CloudMask']), self.INPUT_DIR))

	def test_image_is_croppped(self):
		path = self.INPUT_DIR + '/SkyImage/sgptsiskyimageC1.a1.20131118.131600/' + \
		       'sgptsiskyimageC1.a1.20131118.133000.jpg.20131118133000.jpg'
		shape = crop_image(misc.imread(path)).shape
		self.assertEqual((480, 480, 3), shape)

	def test_mask_path_extracted_from_time(self):
		path = self.INPUT_DIR + '/CloudMask/sgptsicldmaskC1.a1.20131118/' + \
		       'sgptsicldmaskC1.a1.20131118.133230.png.20131118133230.png'
		time = '20131118133230'
		self.assertEqual(path, extract_mask_path_from_time_old(time, self.INPUT_DIR))

	def test_image_path_extracted_from_time(self):
		path = self.INPUT_DIR + '/SkyImage/sgptsiskyimageC1.a1.20131118.131600/' + \
		       'sgptsiskyimageC1.a1.20131118.133000.jpg.20131118133000.jpg'
		time = '20131118133000'
		self.assertEqual(path, extract_img_path_from_time_old(time, self.INPUT_DIR))

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

# def test_batches_are_correct(self):
# 	times = extract_all_times(INPUT_DIR)
# 	blacklist = find_unpaired_images(INPUT_DIR, times)
# 	for b in blacklist:
# 		times.remove(b)
# 	create_dirs(times, OUTPUT_DIR)
# 	times = list(times)
# 	print(len(times))
# 	print(make_batches(times))
# 	self.fail("Help!")
