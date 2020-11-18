import unittest
import config
config.RAW_DATA_DIR = "../test_data"

from clean_csv import *

class TestCleanCsv(unittest.TestCase):

    # TODO We'll need to change the test dates because all our data are from May-July

    def test_finds_raw_photo_path(self):
        self.assertEqual("../test_data/SkyImage/sgptsiskyimageC1.a1.20180418.000000/sgptsiskyimageC1.a1.20180418.000330.jpg.20180418000330.jpg",
                         raw_photo_path("20180418000330"))

    def test_notices_missing_raw_photo_path(self):
        self.assertIsNone(raw_photo_path("19000418000330"))


if __name__ == '__main__':
    unittest.main()
