import os
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def read_netcdf_files(directory = '../ShCu_times'):
    #  Read through the netcdf files and extract the
    #  day, start_hour, end_hour, and two flags.
    # Create a Dataframe containing (day, start_hour, end_hour, event, event_test)
    # Then turn it into a list of Timestamps

    files = os.listdir(directory)
    print(files)
    # initialize output. This will be a dataframe with 5 columns containing:
    # [day, start_hour, end_hour, shallowcumulus_event, shallowcumulus_event_tests]
    dfs = []

    for file in files:
        if file.endswith('.nc'): # Process only NetCDF files
            print(file)
            file_path = os.path.join('../ShCu_times/',file)

            # Open NetCDF data using xarray
            ds = xr.open_dataset(file_path)

            # Read the variables of interest from the NetCDF file
            time1 = ds.time.values
            start_hour = ds.start_hour.values
            end_hour = ds.end_hour.values
            shallowcumulus_event = ds.shallowcumulus_event.values
            shallowcumulus_event_tests = ds.shallowcumulus_event_tests.values

            # make 'time' the same dimension as the others.
            time = np.tile(time1,(4, 1)).transpose()

            # Get only the values corresponding to non-nan start_hour values,
            # and shallowcumulus_event_tests == 0. (no overlying cirrus)
            mask = (~np.isnan(start_hour)) & (shallowcumulus_event_tests == 0)
            tt = time[mask]
            sh = start_hour[mask]
            eh = end_hour[mask]
            ev = shallowcumulus_event[mask].astype('int32')
            tst = shallowcumulus_event_tests[mask]

            # combine in a DataFrame to accommodate different data types.
            df = pd.DataFrame({'day':tt, 'start_hour':sh, 'end_hour':eh, 'event':ev, 'event_test':tst})

            dfs.append(df)
            ds.close()

    # Concatenate all DataFrames into a single DataFrame
    output = pd.concat(dfs, ignore_index=True)

    # turn each row into a list of times with 5M spacing, and flatten the list of lists
    time_intervals = [generate_time_range(row['day'], row['start_hour'], row['end_hour']) for index, row in output.iterrows()]
    shcu_times = [time for sublist in time_intervals for time in sublist]

    return shcu_times

def generate_time_range(day, start_hour, end_hour):
    # Create a list of datetime stamps from start_time to end_time with frequency 5 minutes.
        start_time = day + pd.Timedelta(hours=start_hour)
        end_time = day + pd.Timedelta(hours=end_hour)
        return pd.date_range(start=start_time, end=end_time, freq='5T').tolist()

def read_erin_files(filename):
    # Read Erin's times of ShCu
    df = pd.read_csv(filename, converters={'timestamp_utc': str},
                     usecols=['timestamp_utc','fsc_z','fsc_thn_z','cf_shcu'])

    # sub-sample to every 5M
    mask = df['timestamp_utc'].str.endswith('000') | df['timestamp_utc'].str.endswith('500')
    df = df[mask]
    df['erin_times']=pd.to_datetime(df['timestamp_utc'], format= '%Y%m%d%H%M%S')
    return df

shcu_times = read_netcdf_files()

# Now read Erin's files. Return a dataframe with timestamps and corresponding FSC & CF
typ = read_erin_files('../raw_csv/shcu_typical_data.csv')
dub = read_erin_files('../raw_csv/shcu_dubious_data.csv')

shcu_set = set(shcu_times) # len = 6063
typ_set = set(typ['erin_times']) # len = 10376
dub_set = set(dub['erin_times']) # len = 10376

# Describe the overlap between the two.
LT = len(typ_set)
LD = len(dub_set)
LS = len(shcu_set)
both = shcu_set.intersection(typ_set.union(dub_set))
LB = len(both)
both_typ = typ_set.intersection(shcu_set)
both_dub = dub_set.intersection(shcu_set)
print('VAP finds %d images. %.0d%% are in Erin''s set' % (LS, LB/LS*100))
print('Erin finds %d typical and %d dubious images, of which '
      '%.0d%% and %.0d%% are in the VAP, respectively' %
      (LT, LD, len(both_typ)/LT*100, len(both_dub)/LD*100))

print("Typical images 5 min sampling. Erin: %d; VAP: %d images" % (LT, LS))
print("Overlap: %d images (%.0d%% of Erin's, %.0d%% of VAP)" % (LB, LB/LT*100, LB/LS*100))

both = shcu_set.intersection(dub_set)
LB = len(both)
print("Dubious images 5 min sampling. Erin: %d; VAP: %d images" % (LD, LS))
print("Overlap: %d images (%.0d%% of Erin's, %.0d%% of VAP)" % (LB, LB/LD*100, LB/LS*100))

