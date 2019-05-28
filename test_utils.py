# Unit tests for utils

import unittest
from utils import *


class TestUtil(unittest.TestCase):

	def test_extracts_year_from_time(self):
		self.assertEqual('2017', time_to_year('20170814092430'))


if __name__ == '__main__':
	unittest.main()
