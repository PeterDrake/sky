import pandas as pd
from utils_timestamp import *
from dotenv import load_dotenv
import os
import pysftp
from config import *


class GlareRemover:

    def pull_files(self, timestamps):
        load_dotenv()
        user = os.environ.get('user')
        password = os.environ.get('password')
        with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
            for t in timestamps:
                connection.get(f'{DATA_DIR}/photos/{yyyymmdd(t)}/{t}_photo.jpg',
                               f'../data_for_plotting/{t}_photo.jpg')
                connection.get(f'{DATA_DIR}/tsi_masks/{yyyymmdd(t)}/{t}_tsi_mask.png',
                               f'../data_for_plotting/{t}tsi_mask.png')

    def has_glare(self, timestamps, fscs):
        hours = timestamps.map(lambda t: int(hhmmss(t)[:2]))
        # print(hours.value_counts())
        return (fscs < 0.1) & ((hours < 17) | (hours >= 23))

    def find_glare_files(self, csv):
        result = pd.read_csv(csv, converters={'timestamp_utc': str})
        result['total'] = result['clear_100'] + result['thin_100'] + result['opaque_100']
        result['fsc_thin_100'] = result['thin_100'] / result['total']
        result['fsc_opaque_100'] = result['opaque_100'] / result['total']
        result['glare'] = self.has_glare(result['timestamp_utc'], result['fsc_thin_100'] + result['fsc_opaque_100'])
        # print(self.counts)
        print(result['glare'].mean())
        self.pull_files(list(result[result['glare']]['timestamp_utc'])[::100])

g = GlareRemover()
g.find_glare_files('../data_for_plotting/typical_validation_tsi_fsc.csv')
