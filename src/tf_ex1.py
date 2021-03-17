# This file works through exercises in 'Hands-on machine learning with Scikit-Learn, Keras, and TensorFlow' O'Reilly book.

# All of the code is available on a GitHub repository.
# We are in Chap 10.
# https://github.com/ageron/handson-ml2

# Summary:
# model = keras.models.Sequential([ ...
# model.compile()
# model.fit()
# model.save

import tensorflow as tf
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()
# The mnist dataset is a famous dataset of fashion images.

X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.0

# names of classes [0:9]
class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# define the network. Note it's a single sequential model.
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

# check it out with:
# model
# model.summary()
# hidden1 = model.layers[1]
# weights,biases = hidden1.get_weights()
# weights.shape
# biases.shape

# Compile the model:
model.compile(loss="sparse_categorical_crossentropy",
              optimizer="sgd",
              metrics=["accuracy"])

# sgd = stochastic gradient descent.

# Train the model.
history = model.fit(X_train, y_train, epochs=30, validation_data=(X_valid, y_valid))

# Visualize model errors.
pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
save_fig("keras_learning_curves_plot")
plt.show()

# Evaluate the model.
model.evaluate(X_test, y_test)

# See how confident the model is in its predictions

X_new = X_test[:3]
y_pred = np.argmax(model.predict(X_new), axis=-1)

# See the predictions for any of the inputs
y_pred = model.predict_classes(X_new)
np.array(class_names)[y_pred]


# Save the model!
model.save('tf_ex1_fashion_model')