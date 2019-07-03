from unittest import TestCase
from utils import *
from replace_green_lines import new_remove_green

class TestRemove_green(TestCase):

	def test_remove_green(self):
		mask = np.asarray([[BLACK, BLUE, BLACK, BLUE, BLUE],
						  [BLACK, BLUE, GREEN, WHITE, GRAY],
						  [BLACK, BLUE, GREEN, GREEN, WHITE],
						  [BLUE, WHITE, WHITE, GREEN, GRAY],
						  [BLACK, BLUE, GRAY, BLACK, GRAY]], dtype=np.uint8)

		answer_mask = np.asarray([[BLACK, BLUE, BLACK, BLUE, BLUE],
						   		  [BLACK, BLUE, BLUE, WHITE, GRAY],
						   		  [BLACK, BLUE, WHITE, WHITE, WHITE],
						   		  [BLUE, WHITE, WHITE, GRAY, GRAY],
						   		  [BLACK, BLUE, GRAY, BLACK, GRAY]], dtype=np.uint8)

		imageio.imwrite('typical_data/test_remove_green.png', mask)

		new_mask = new_remove_green(mask)

		self.assertTrue(np.all(answer_mask == new_mask))

		imageio.imwrite('typical_data/test_remove_green_result.png', new_mask)
