from utils_image import *
import unittest
import numpy as np
import matplotlib.pyplot as plt


class TestUtilsImage(unittest.TestCase):

    def circle(self, r_center, c_center, radius):
        """
        Returns a mask with a circle centered at r, c with the specified radius.
        """
        circle = np.fromfunction(lambda r, c, _: (r - r_center) ** 2 + (c - c_center) ** 2 <= radius ** 2, (640, 480, 3))
        blue = np.full((640, 480, 3), (0, 0, 255))  # TODO Colors and standard shape should be constants
        black = np.full((640, 480, 3), (0, 0, 0))
        return np.where(circle, blue, black)

    def test_finds_circle_edges(self):
        tiny = self.circle(300, 200, 100)
        self.assertEqual((200, 400, 100, 300), circle_edges(tiny))

    def test_finds_center_and_radius(self):
        tiny = self.circle(300, 200, 100)
        (r, c), radius = center_and_radius(tiny)
        self.assertEqual(300, r)
        self.assertEqual(200, c)
        self.assertEqual(100, radius)

    def test_crops_mask(self):
        tiny = self.circle(300, 200, 100)
        coords = center_and_radius(tiny)
        cropped = crop_mask(tiny, coords)
        # To see the image, uncomment these lines
        # plt.imshow(cropped)
        # plt.show()
        self.assertEqual((480, 480, 3), cropped.shape)
        (r, c), radius = center_and_radius(cropped)
        self.assertEqual(240, r)
        self.assertEqual(240, c)
        self.assertEqual(100, radius)

    def test_crops_offset_circle(self):
        tiny = self.circle(150, 300, 149)
        coords = center_and_radius(tiny)
        cropped = crop_mask(tiny, coords)
        # To see the image, uncomment these lines
        # plt.imshow(cropped)
        # plt.show()
        self.assertEqual((480, 480, 3), cropped.shape)
        (r, c), radius = center_and_radius(cropped)
        self.assertEqual(240, r)
        self.assertEqual(240, c)
        self.assertEqual(149, radius)


if __name__ == '__main__':
    unittest.main()
