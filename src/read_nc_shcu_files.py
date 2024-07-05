import os
import pandas as pd
import xarray as xr
import numpy as np

# First just read through the netcdf files and extract the day, start_hour, end_hour, and two flags.
def read_netcdf_files(directory = '../ShCu_times'):
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

            # Get only the values corresponding to non-nan start_hour values
            mask = ~np.isnan(start_hour)
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
    return output

def df_to_timestamp():



# Create a Dataframe containing (day, start_hour, end_hour, event, event_test)
output = read_netcdf_files()

# Convert this into a list of times every 5 minutes.
shcu_times = df_to_timestamp()

# Get the times for our analysis

a="hi"
