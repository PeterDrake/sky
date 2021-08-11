class FscCalculator:

    def count_pixels(self, mask, color):
        """
        Returns the number of pixels in image which are of color.
        :param mask: 480x480x3 numpy array
        :param color: 3 element numpy array
        """
        return (mask == color).all(axis=2).sum()
