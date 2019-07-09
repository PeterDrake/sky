from tensorflow._api.v1.keras.models import load_model
import matplotlib.pyplot as plt
from train_model_1 import *

model = load_model('model_1_20.h5')
# summarize model.
model.summary()
# load dataset
history = model.fit_generator(generator=training_batch_generator,
						steps_per_epoch=len(train_stamps) // TRAINING_BATCH_SIZE, epochs=2, verbose=1,
						validation_data=validation_batch_generator,
						validation_steps=len(valid_stamps) // TRAINING_BATCH_SIZE,
						use_multiprocessing=False, callbacks=[cb_1, tensorboard])

# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()