import pandas as pd
from utils_timestamp import *
from config import *


class TimestampAllocator:

    def __init__(self, data_dir, typical_proportions, dubious_proportions=None, verbose=True):
        self.data_dir = data_dir
        self.typical_proportions = typical_proportions
        self.dubious_proportions = dubious_proportions
        self.verbose = verbose

    def log(self, message):
        if self.verbose:
            print(message)

    def count_images_per_date(self, csv_filename):
        """
        Returns a DataFrame associating dates (strings in yyyymmdd format) with the numbers of timestamps within each
        of those dates, with columns 'date' and 'count'.
        :param csv_filename: in self.data_dir
        """
        # Read the CSV file
        csv = self.data_dir + '/' + csv_filename
        self.log('Reading ' + csv)
        data = pd.read_csv(csv, converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
        # Add a date column
        data['date'] = data['timestamp_utc'].map(yyyymmdd)
        # Count timestamps for each date
        grouped = data.groupby('date').count()
        # Convert the DataFrame to a dictionary
        grouped = grouped.reset_index()
        grouped.rename(columns={'timestamp_utc': 'count'}, inplace=True)
        return grouped

    def allocate_timestamps_helper(self, csv_filename, proportions, output_filenames):
        """
        Divides the timestamps in csv_filename (which is in self.data_dir) randomly according to proportions.
        The timestamps are then written into the files specified by output_filenames.
        :param proportions: a list of numbers summing to 1.0, corresponding to output_filenames.
        """
        csv = self.data_dir + '/' + csv_filename
        self.log('Reading ' + csv)
        data = pd.read_csv(csv, converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
        data['date'] = data['timestamp_utc'].map(yyyymmdd)
        self.log('Allocating timestamps')
        date_counts = self.count_images_per_date(csv_filename)
        date_groups = allocate_dates(date_counts, proportions)
        self.log('Writing timestamp files')
        for group, filename in zip(date_groups, output_filenames):
            print('Creating timestamp file ' + filename)
            df = data[data['date'].isin(group)]
            df['timestamp_utc'].to_csv(self.data_dir + '/' + filename, header=False, index=False)
        self.log('Done')

    def allocate_timestamps(self, csv_filename, typical_or_dubious):
        """
        Divides the timestamps in csv_filename (which is in self.data_dir) randomly into groups.
        The timestamps are then written into files. The group proportions are specified in the constructor for this
        class.
        :param typical_or_dubious: True to use typical data, False to use dubious data
        """
        if typical_or_dubious == 'typical':
            self.allocate_timestamps_helper(csv_filename, self.typical_proportions, TYPICAL_TIMESTAMP_FILENAMES)
        else:
            self.allocate_timestamps_helper(csv_filename, self.dubious_proportions, DUBIOUS_TIMESTAMP_FILENAMES)
