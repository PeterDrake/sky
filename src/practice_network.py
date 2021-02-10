import tensorflow as tf
from tensorflow import keras
import random
import matplotlib.pyplot as plt
import numpy as np
from utils_timestamp import *
from utils_image import *

# Load the dataset
# with open('../test_data/typical_training_timestamps') as f:
#     train_stamps = f.read().splitlines()
# random.shuffle(train_stamps)
# train_stamps = train_stamps[:10]


def load_photo(timestamp):
    # TODO We'll need a method for this
    # TODO It also has some redundancy with Preprocessor.preprocess_timestamp
    photo = plt.imread('../test_data/photos/' + yyyymmdd(timestamp) + '/' + timestamp + '_photo.jpg')
    return np.array(photo, dtype='uint8')  # TODO Do we need to divide by 255.0?


train_stamps = ['20180418000200', '20180419000200']
train_photos = [load_photo(timestamp) for timestamp in train_stamps]
X_train = np.stack(train_photos)


def load_mask(timestamp):
    # TODO We'll need a method for this
    # TODO It also has some redundancy with Preprocessor.preprocess_timestamp
    mask = plt.imread('../test_data/tsi_masks/' + yyyymmdd(timestamp) + '/' + timestamp + '_tsi_mask.png')
    return rgb_to_one_hot_mask(np.array(mask * 255, dtype='uint8')[:, :, :3])

train_masks = [load_mask(timestamp) for timestamp in train_stamps]
y_train = np.stack(train_masks)



print([p.shape for p in train_masks])

# fashion_mnist = keras.datasets.fashion_mnist
# (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()
#
# # Separate validation set
# X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
# y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
# X_test = X_test / 255.0
#
# # Names of classes
# class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
#                "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]
#
# # Define the network
# model = keras.models.Sequential([
#     keras.layers.Flatten(input_shape=[28, 28]),
#     keras.layers.Dense(300, activation="relu"),
#     keras.layers.Dense(100, activation="relu"),
#     keras.layers.Dense(10, activation="softmax")
# ])
#
# # Compile the model
# model.compile(loss="sparse_categorical_crossentropy",
#               optimizer="sgd",
#               metrics=["accuracy"])
#
# # Train the model
# history = model.fit(X_train, y_train, epochs=30, validation_data=(X_valid, y_valid))
#
# # Plot learning curves
# import pandas as pd
# import matplotlib.pyplot as plt
#
# pd.DataFrame(history.history).plot(figsize=(8, 5))
# plt.grid(True)
# plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]
# plt.show()


# Make some predictions
# We might do this
# X_new = X_test[:3]
# y_proba = model.predict(X_new)
# y_proba.round(2)
