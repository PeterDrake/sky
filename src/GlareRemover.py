import pandas as pd
from utils_timestamp import *
from collections import defaultdict

class GlareRemover:

    def has_glare(self, timestamps, fscs):
        hours = timestamps.map(lambda t: int(hhmmss(t)[:2]))
        print(hours.value_counts())
        return (fscs < 0.2) & ((hours < 17) | (hours >= 23))

    def find_glare_files(self, csv):
        result = pd.read_csv(csv, converters={'timestamp_utc': str})
        result['total'] = result['clear_100'] + result['thin_100'] + result['opaque_100']
        result['fsc_thin_100'] = result['thin_100'] / result['total']
        result['fsc_opaque_100'] = result['opaque_100'] / result['total']
        result['glare'] = self.has_glare(result['timestamp_utc'], result['fsc_thin_100'] + result['fsc_opaque_100'])
        # print(self.counts)
        print(result['glare'].mean())

g = GlareRemover()
g.find_glare_files('../data_for_plotting/typical_validation_tsi_fsc.csv')
