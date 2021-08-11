from utils_image import *

class FscCalculator:

    def count_pixels(self, mask):
        """
        Returns the number of blue, gray and white pixels in mask.
        :param mask: 480x480x3 numpy array
        """
        return [(mask == c).all(axis=2).sum() for c in [BLUE, GRAY, WHITE]]




# 1) Create an object instance that includes directory names
# 2) Build paths ... functions that can call network_mask_path, timestamp_path, csv_path
# 3) Read in the stamps for desired masks (eg. typical_validation_timestamps) as a list of strings
# 4) For each stamp, read the corresponding network_mask,
#   a) return total count of sky, white & gray.
#   b) return count of sky, white & gray inside 100-deg circle.
# 5) construct a DataFrame
# 6) write to .csv file.

# df = pd.DataFrame(index=val_stamps, columns = ('clear_160', 'thin_160', 'opaque_160', 'clear_100', 'thin_100', 'opaque_100'))
# for stamp in val_stamps:
#     mask = imread(self.raw_tsi_mask_path(timestamp))[:, :, :3] # re-write.
#     counts_160 = count_pixel_values(mask) # in the full mask
#     counts_100 # count pixel values in 100-deg circle.
#     df.loc[stamp] = counts_160 + counts_100
#
# output_csv = pd.DataFrame({'timestamp':stamp,'sky':sky}) # re-write
