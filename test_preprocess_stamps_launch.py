# Unit tests for utils

import unittest
from preprocess_stamps_launch import *
from utils import *


class TestPreprocessStampsLaunch(unittest.TestCase):

	def test_create_constant_mask(self):
		# image with top bar of blue
		test_mask_1 = np.full((480, 480, 3), BLACK)
		test_mask_1[:200] = BLUE
		Image.fromarray(test_mask_1.astype('uint8')).save('test_data/test_images/test_img_1.png')
		# image with middle bar of blue
		test_mask_2 = np.full((480, 480, 3), BLACK)
		test_mask_2[200:400] = BLUE
		Image.fromarray(test_mask_2.astype('uint8')).save('test_data/test_images/test_img_2.png')
		# create constant mask using test masks 1 and 2
		create_constant_mask(BLACK, 'test_data/test_images/created_img.png', 'test_data/test_images/')
		# image with both bars of blue
		test_mask_3 = np.full((480, 480, 3), BLACK)
		test_mask_3[:400] = BLUE
		Image.fromarray(test_mask_3.astype('uint8')).save('test_data/test_images/test_img_3.png')
		# load created image
		img = Image.open('test_data/test_images/created_img.png')
		img.load()
		self.assertEqual(test_mask_3.all(), np.asarray(img).all())




