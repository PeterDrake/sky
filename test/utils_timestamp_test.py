from utils_timestamp import *
import unittest


class MyTestCase(unittest.TestCase):

    def test_extracts_yyyymmdd(self):
        self.assertEqual('20180419', yyyymmdd('20180419010230'))


if __name__ == '__main__':
    unittest.main()
