from config import *
from random import shuffle
from utils import *
import time


def create_dirs(timestamps, output_dir, res_dir):
    """Creates directories for simpleimage and simplemask in the output_dir as well as creating subdirectories by year
	and day for the given timestamps. Expects the input_dir and output_dir to be relative to the current working
	directory. Pass in an iterable collection of timestamps in the yyyymmddhhmmss format."""
    seen = {}
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)
    for t in timestamps:
        year = time_to_year(t)
        mmdd = time_to_month_and_day(t)
        if year not in seen.keys():
            seen[year] = set()
        seen[year].add(mmdd)
    for year in seen.keys():
        os.makedirs(output_dir + "/simpleimage/" + year, exist_ok=True)
        os.makedirs(output_dir + "/simplemask/" + year, exist_ok=True)
        for mmdd in seen[year]:
            os.makedirs(output_dir + "/simpleimage/" + year + "/" + mmdd, exist_ok=True)
            os.makedirs(output_dir + "/simplemask/" + year + "/" + mmdd, exist_ok=True)


def make_batches_by_size(timestamps, batch_size=PREPROCESS_BATCH_SIZE):
    """Returns a set of batches of timestamps for preprocessing."""
    timestamps = list(timestamps)
    num_batches = math.ceil(len(timestamps) / batch_size)
    shuffle(timestamps)  # TODO: If this is just for preprocessing, why bother shuffling?
    time_batches = []
    for i in range(int(num_batches) - 1):
        time_batches += [timestamps[i * batch_size:(i + 1) * batch_size]]
    time_batches.append(timestamps[(num_batches - 1) * batch_size:])
    return time_batches


def setup(output_dir, timestamp_data_csv):
    """
    Creates nested year and day directories for results and files containing timestamps for each batch.
    :param output_dir: Directory where all of the new directories and files will be created.
    :param timestamp_data_csv: File containing all timestamps.
    """
    res_dir = output_dir + '/res'
    print("Cleaning the csv file.")
    clean_csv(timestamp_data_csv)
    print("Reading times from csv file.")
    timestamps = extract_data_from_csv(timestamp_data_csv, "timestamp_utc")
    # This can be used to process a small number of images instead of everything specified by the csv files.
    if SMALL_PROCESS_SIZE:
        print("Reducing the number of timestamps to ", SMALL_PROCESS_SIZE)
        few_times = set()
        count = 0
        for t in timestamps:
            few_times.add(t)
            count += 1
            if count == SMALL_PROCESS_SIZE:
                break
        timestamps = few_times
    print("Finished reading times. Eliminating unpaired times.")
    times = timestamps - find_unpaired_images(timestamps, RAW_DATA_DIR)
    if len(times) == 0:
        print()
        print("ERROR: No paired images and masks found. Please check paths and settings in config.py and make sure "
              + "that the raw data is available.")
        exit(-1)
    print("{} paired images and masks found.".format(len(times)))
    print("Creating directories for results.")
    create_dirs(times, output_dir, res_dir)
    print("Directories created. Preparing batches.")
    batches = make_batches_by_size(times)
    print("Batches prepared. Writing batches to file.")
    for i in range(len(batches)):
        name = res_dir + "/batch" + str(i) + ".txt"
        f = open(name, 'w')
        print("Writing batch {} data to {}".format(i, name))
        for time in batches[i]:
            f.write(time + '\n')
        f.close()
    print("Timestamp files complete.")


if __name__ == '__main__':
    start = time.clock()
    setup(TYPICAL_DATA_DIR, TYPICAL_DATA_CSV)
    setup(DUBIOUS_DATA_DIR, DUBIOUS_DATA_CSV)
    print("Time elapsed: " + str(time.clock() - start) + " seconds.")
