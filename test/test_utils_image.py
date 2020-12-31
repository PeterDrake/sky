from utils_image import *
import unittest
import numpy as np
import matplotlib.pyplot as plt


class TestUtilsImage(unittest.TestCase):

    def add_circle(self, r_center, c_center, radius, color=BLUE, image=np.full((640, 480, 3), BLACK)):
        """
        Returns an image with a circle of the specified color centered at r_center, c_center with the
        specified radius.
        :param image If specified, use this for anything outside the circle; otherwise use 640x480x3 all black.
        """
        circle = np.fromfunction(lambda r, c, _: (r - r_center) ** 2 + (c - c_center) ** 2 <= radius ** 2, image.shape)
        return np.where(circle, color, image)

    def test_finds_circle_edges(self):
        mask = self.add_circle(300, 200, 100)
        self.assertEqual((200, 400, 100, 300), circle_edges(mask))

    def test_finds_center_and_radius(self):
        mask = self.add_circle(300, 200, 100)
        (r, c), radius = center_and_radius(mask)
        self.assertEqual(300, r)
        self.assertEqual(200, c)
        self.assertEqual(100, radius)

    def test_crops(self):
        mask = self.add_circle(300, 200, 100)
        coords = center_and_radius(mask)
        cropped = crop(mask, coords)
        # To see the image, uncomment these lines
        # plt.imshow(cropped)
        # plt.show()
        self.assertEqual((480, 480, 3), cropped.shape)
        (r, c), radius = center_and_radius(cropped)
        self.assertEqual(240, r)
        self.assertEqual(240, c)
        self.assertEqual(100, radius)

    def test_crops_offset_circle(self):
        mask = self.add_circle(150, 300, 149)
        coords = center_and_radius(mask)
        cropped = crop(mask, coords)
        # To see the image, uncomment these lines
        # plt.imshow(cropped)
        # plt.show()
        self.assertEqual((480, 480, 3), cropped.shape)
        (r, c), radius = center_and_radius(cropped)
        self.assertEqual(240, r)
        self.assertEqual(240, c)
        self.assertEqual(149, radius)

    def test_blackens_outer_ring(self):
        mask = self.add_circle(300, 200, 100)
        coords = center_and_radius(mask)
        photo = np.random.randint(0, 255, (480, 480, 3))
        # To see the image, uncomment these lines
        # plt.imshow(before)
        # plt.show()
        after = blacken_outer_ring(photo, coords)
        # To see the image, uncomment these lines
        # plt.imshow(after)
        # plt.show()
        self.assertTrue((np.zeros(3) == after[5, 5, :]).all())

    def test_mask_and_photo_correspond_after_cropping_and_black_outer_ring(self):
        mask = self.add_circle(300, 200, 100, WHITE)
        coords = center_and_radius(mask)
        cropped_mask = crop(mask, coords)
        # The integers start at 1 to avoid an accidental black pixels
        photo = np.random.randint(1, 255, (480, 480, 3))
        photo = crop(photo, coords)
        photo = blacken_outer_ring(photo, coords)
        self.assertTrue(((cropped_mask == BLACK) == (photo == BLACK)).all())

    def test_removes_yellow_sun(self):
        mask = self.add_circle(300, 200, 100, WHITE)
        yellow_sun = self.add_circle(250, 150, 25, YELLOW, mask)
        black_sun = self.add_circle(250, 150, 25, BLACK, mask)
        coords = center_and_radius(yellow_sun)
        cropped_mask = crop(yellow_sun, coords)
        black_sun = crop(black_sun, coords)
        after = remove_sun(cropped_mask)
        # To see the image, uncomment these lines
        # plt.imshow(after)
        # plt.show()
        self.assertTrue((black_sun == after).all())

    def test_removes_white_sun(self):
        mask = self.add_circle(300, 200, 100, WHITE)
        mask = self.add_circle(250, 150, 50, BLACK, mask)  # Fake shadowband
        mask = self.add_circle(350, 250, 5, GREEN, mask)  # Fake TSI segmentation "line"
        mask = self.add_circle(330, 250, 5, GRAY, mask)  # Fake thin cloud
        mask = self.add_circle(310, 250, 5, BLUE, mask)  # Fake clear sky
        white_sun = self.add_circle(250, 150, 25, WHITE, mask)
        coords = center_and_radius(white_sun)
        black_sun = crop(mask, coords)
        cropped_mask = crop(white_sun, coords)
        after = remove_sun(cropped_mask)
        # To see the image, uncomment these lines
        # plt.imshow(after)
        # plt.show()
        self.assertTrue((black_sun == after).all())


if __name__ == '__main__':
    unittest.main()
