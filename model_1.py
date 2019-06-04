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


sky_images = Input(shape=(480, 480, 3), name='SkyImages')
first_conv = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='FirstConvolution')(sky_images)

first_maxpool = Lambda(lambda x: tf.nn.max_pool(first_conv, [1, 1, 100, 1], strides=[1, 1, 1, 1], padding='SAME'), name='FirstMaxPool')(first_conv)
second_maxpool = Lambda(lambda x: tf.nn.max_pool(first_conv, [1, 100, 1, 1], strides=[1, 1, 1, 1], padding='SAME'), name='SecondMaxPool')(first_conv)

merge_one = concatenate([first_conv, first_maxpool], axis=3)
merge_two = concatenate([second_maxpool, merge_one], axis=3)

second_conv = Convolution2D(filters=32, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='SecondConvolution')(merge_two)

merge_three = concatenate([second_conv, sky_images], axis=3)

third_conv = Convolution2D(filters=4, kernel_size=3, padding='same', data_format='channels_last', activation='relu', name='ThirdConvolution')(merge_three)

mask_layer = Lambda(lambda x: mask_layer(third_conv, b_mask), name='MaskLayer')(third_conv)

reshape_layer = Lambda(lambda x: tf.reshape(mask_layer, [-1, 4]), name='Reshape')(mask_layer)

tsi = Input(shape=[None], dtype='int64', name='TSIDecisionImages')

nongreen_layer = Lambda(lambda x: tf.not_equal(tsi, 4), name='NonGreenLayer')(tsi)

network_boolean = Lambda(lambda x: tf.boolean_mask(reshape_layer, nongreen_layer), name='NetworkBoolean')([reshape_layer, nongreen_layer])

tsi_boolean = Lambda(lambda x: tf.boolean_mask(tsi, nongreen_layer), name='TSIBoolean')([tsi, nongreen_layer])

s_s_cross_entropy_w_l = Lambda(lambda x: tf.nn.softmax_cross_entropy_with_logits(labels=tsi_boolean, logits=network_boolean), name='SparseSoftmaxCrossEntropy')([tsi_boolean, network_boolean])

cross_entropy = Lambda(lambda x: tf.reduce_mean(s_s_cross_entropy_w_l), name='CrossEntropy')(s_s_cross_entropy_w_l)

arg_max = Lambda(lambda x: tf.argmax(network_boolean, 1), name='ArgMax')(network_boolean)

correct_prediction = Lambda(lambda x: tf.equal(arg_max, tsi_boolean), name='CorrectPrediction')([arg_max, tsi_boolean])

cast = Lambda(lambda x: tf.cast(correct_prediction, tf.float32), name='Cast')(correct_prediction)

accuracy = Lambda(lambda x: tf.reduce_mean(cast), name='Accuracy')(cast)

model = Model(inputs=[sky_images, tsi], outputs=[cross_entropy, accuracy])

model.summary()
plot_model(model, show_shapes=True, to_file='model_1.png')