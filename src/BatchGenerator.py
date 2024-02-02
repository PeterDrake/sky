from tensorflow import keras
from utils_timestamp import *
from utils_image import *
import numpy as np
from skimage.io import imsave, imread


class BatchGenerator(keras.utils.Sequence):
    """Loads batches of data (each batch as an Nx480x480x3 numpy array) for network training."""

    def __init__(self, timestamps, data_dir, batch_size=16, use_no_glare_masks=False):
        """
        :param timestamps: List of timestamps for the data to be put into batches.
        :param data_dir: Directory where the data live, containing photos and tsi_masks.
        :param batch_size: Number of images in each batch.
        """
        self.timestamps = timestamps
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.use_no_glare_masks = use_no_glare_masks

    def __len__(self):
        """
        Returns number of batches (not number of images) in the data rounded up.
        Since Python does not have a ceiling division function, we use floor division on negative values.
        https://newbedev.com/is-there-a-ceiling-equivalent-of-operator-in-python
        """
        return -(-len(self.timestamps) // self.batch_size)

    def __getitem__(self, index):
        """
        Returns tuple (photos, labeled TSI masks) corresponding to batch #index.
        Dimension of photo_batch is (batch_size x 480 x 480 x 3).
        Dimension of tsi_mask_batch is (batch_size x 480 x 480 x 1).
        """
        i = index * self.batch_size  # Index of the beginning of the batch
        batch_timestamps = self.timestamps[i : i + self.batch_size]  # Timestamps for this batch
        n = len(batch_timestamps)
        photo_paths = [timestamp_to_photo_path(self.data_dir, t) for t in batch_timestamps]
        if self.use_no_glare_masks:
            tsi_mask_paths = [timestamp_to_tsi_mask_no_glare_path(self.data_dir, t) for t in batch_timestamps]
        else:
            tsi_mask_paths = [timestamp_to_tsi_mask_path(self.data_dir, t) for t in batch_timestamps]
        print("Getting TSI masks from " + tsi_mask_paths)
        photo_batch = np.zeros((n,) + RGB_PHOTO_SIZE, dtype="uint8")  # Shape (N, 480, 480, 3)
        for j, path in enumerate(photo_paths):
            photo_batch[j] = imread(path)
        tsi_mask_batch = np.zeros((n,) + LABELED_MASK_SIZE, dtype="uint8")  # Shape (N, 480, 480, 1)
        for j, path in enumerate(tsi_mask_paths):
            rgb = imread(path)  # Shape (480, 480, 3)
            # print("Reading rgb image of tsi mask: ", rgb.shape, rgb.dtype)
            labeled = rgb_mask_to_label(rgb)  # Shape (480, 480)
            tsi_mask_batch[j] = np.expand_dims(labeled, 2)  # Shape (480, 480, 1)
        return photo_batch, tsi_mask_batch
