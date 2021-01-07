from utils_timestamp import *
import unittest


class TestUtilsTimestamp(unittest.TestCase):

    def test_extracts_yyyymmdd(self):
        self.assertEqual('20180419', yyyymmdd('20180419010230'))

    def test_extracts_hhmmss(self):
        self.assertEqual('010230', hhmmss('20180419010230'))

    def test_allocates_dates(self):
        days = [str(d) for d in range(100)]
        counts = ([1] * 70) + ([3] * 30)
        dates = pd.DataFrame.from_dict({'date': days, 'count': counts})
        train, test = allocate_dates(dates, [0.8, 0.2])
        total_count = sum(counts)
        train_count = dates[dates['date'].isin(train)].sum()['count']
        test_count = dates[dates['date'].isin(test)].sum()['count']
        self.assertTrue(0.75 < train_count / total_count < 0.85)
        self.assertTrue(0.15 < test_count / total_count < 0.25)


if __name__ == '__main__':
    unittest.main()
