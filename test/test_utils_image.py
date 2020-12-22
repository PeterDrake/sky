from utils_image import *
import unittest
import numpy as np
import matplotlib.pyplot as plt


class TestUtilsImage(unittest.TestCase):

    def setUp(self):
        circle = np.fromfunction(lambda r, c, _: (r-300)**2 + (c-200)**2 <= 100**2, (640, 480, 3))
        blue = np.full((640, 480, 3), (0, 0, 255))  # TODO Colors and standard shape should be constants
        black = np.full((640, 480, 3), (0, 0, 0))
        self.tiny = np.where(circle, blue, black)
        # To see the tiny image, uncomment these lines
        # plt.imshow(self.tiny)
        # plt.show()

    def test_finds_circle_edges(self):
        self.assertEqual((200, 400, 100, 300), circle_edges(self.tiny))

    def test_finds_center_and_radius(self):
        (r, c), radius = center_and_radius(self.tiny)
        self.assertEqual(300, r)
        self.assertEqual(200, c)
        self.assertEqual(100, radius)


if __name__ == '__main__':
    unittest.main()
