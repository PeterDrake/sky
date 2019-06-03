import numpy as np
from keras.models import Model
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D, concatenate, Input, Lambda
from keras.utils import np_utils, plot_model
import tensorflow as tf
from matplotlib import pyplot as plt
from config import *
from train import *

np.random.seed(123)  # for reproducibility

b_mask = color_mask(np.asarray(imageio.imread(TYPICAL_DATA_DIR + '/always_black_mask.png')), index_of(BLACK, COLORS))

def max_pool(prev, width, height):
    return tf.nn.max_pool(prev, [1, width, height, 1], strides=[1, 1, 1, 1], padding='SAME')


first_input = Input(shape=(480, 480, 3), name='Input')
first_conv = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='FirstConvolution')(first_input)

first_maxpool = Lambda(lambda x: max_pool(first_conv, 1, 100), name='FirstMaxPool')(first_conv)
second_maxpool = Lambda(lambda x: max_pool(first_conv, 100, 1), name='SecondMaxPool')(first_conv)

merge_one = concatenate([first_conv, first_maxpool], axis=3)
merge_two = concatenate([second_maxpool, merge_one], axis=3)

second_conv = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='SecondConvolution')(merge_two)

merge_three = concatenate([second_conv, first_input], axis=3)

third_conv = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='ThirdConvolution')(merge_three)

mask_layer = Lambda(lambda x: mask_layer(third_conv, b_mask), name='MaskLayer')(third_conv)

model = Model(inputs=[first_input], outputs=mask_layer)

model.summary()