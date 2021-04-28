from tensorflow import keras
from utils_timestamp import *
from utils_image import *
import numpy as np
import matplotlib.pyplot as plt


class BatchGenerator(keras.utils.Sequence):
    """Loads batches of data (each batch as an Nx480x480x3 numpy array) for network training."""

    def __init__(self, timestamps, data_dir, batch_size=32):
        """
        :param timestamps: List of timestamps for the data to be put into batches.
        :param data_dir: Directory where the data live, containing photos and tsi_masks.
        :param batch_size: Number of images in each batch.
        """
        self.timestamps = timestamps
        self.data_dir = data_dir
        self.batch_size = batch_size

    def __len__(self):
        """
        Returns number of batches (not number of images) in the data.
        """
        return len(self.timestamps) // self.batch_size

    def __getitem__(self, index):
        """Returns tuple (photo, labeled TSI mask) correspond to batch #index."""
        i = index * self.batch_size  # Index of the beginning of the batch
        batch_timestamps = self.timestamps[i : i + self.batch_size]  # Timestamps for this batch
        photo_paths = [timestamp_to_photo_path(self.data_dir, t) for t in batch_timestamps]
        tsi_mask_paths = [timestamp_to_tsi_mask_path(self.data_dir, t) for t in batch_timestamps]
        # TODO We sure do say (480, 480, 3) a lot. Define a constant somewhere?
        photo_batch = np.zeros((self.batch_size,) + (480, 480, 3), dtype="float32")  # Shape (N, 480, 480, 3)
        for j, path in enumerate(photo_paths):
            photo_batch[j] = plt.imread(path)
        tsi_mask_batch = np.zeros((self.batch_size,) + (480, 480, 1), dtype="uint8")  # Shape (N, 480, 480, 1)
        for j, path in enumerate(tsi_mask_paths):
            rgb = plt.imread(path)  # Shape (480, 480, 3)
            labeled = rgb_mask_to_label(rgb)  # Shape (480, 480)
            tsi_mask_batch[j] = np.expand_dims(labeled, 2)  # Shape (480, 480, 1)
        return photo_batch, tsi_mask_batch
