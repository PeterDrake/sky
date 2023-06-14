import pandas as pd
from WindowFinder import *

# TODO Combine this with WindowFinder
class FscAverager:

    def __init__(self, data_dir, fsc_filename, half_width=7.5, min_stamps=25):
        self.data_dir = data_dir
        path = self.data_dir + '/' + fsc_filename
        self.wf = WindowFinder(path, half_width, min_stamps)
        self.data = pd.read_csv(path, index_col=0)

    def compute_averages(self, year):
        windows = self.wf.find_windows(year)
        data = []
        for stamp, (start, end) in windows.items():
            sums = self.data.iloc[start:end+1].sum()
            sums['timestamp_utc'] = stamp
            data.append(sums)
        result = pd.DataFrame(data)
        result['total'] = result['clear_100'] + result['thin_100'] + result['opaque_100']
        result['fsc_thin_100'] = result['thin_100'] / result['total']
        result['fsc_opaque_100'] = result['opaque_100'] / result['total']
        return result[['timestamp_utc', 'fsc_thin_100', 'fsc_opaque_100']]
