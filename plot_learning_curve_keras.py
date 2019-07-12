from tensorflow._api.v1.keras.models import load_model
import matplotlib.pyplot as plt
from train_model_1 import *

model = load_model('model_1_20.h5')
# summarize model.
model.summary()
# load dataset

with open(TYPICAL_DATA_DIR + '/train.stamps', 'rb') as f:
	train_stamps = pickle.load(f)
print('Training stamps loaded.')
with open(TYPICAL_VALID_FILE, 'rb') as f:
	valid_stamps = pickle.load(f)
print('Validation stamps loaded.')

training_image_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, False)
print('Training image file paths loaded.')
print(len(training_image_filenames))
training_tsi_filenames = load_filenames(train_stamps, TYPICAL_DATA_DIR, True)
print('Training mask file paths loaded.')
print(len(training_tsi_filenames))
validation_image_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, False)
print('Validation image file paths loaded.')
validation_tsi_filenames = load_filenames(valid_stamps, TYPICAL_DATA_DIR, True)
print('Validation mask file paths loaded.')

training_batch_generator = Image_Generator(training_image_filenames, training_tsi_filenames, TRAINING_BATCH_SIZE)
print('Training generator initialized.')
validation_batch_generator = Image_Generator(validation_image_filenames, validation_tsi_filenames, TRAINING_BATCH_SIZE)
print('Validation generator initialized.')

history = model.fit_generator(generator=training_batch_generator,
						steps_per_epoch=len(train_stamps) // TRAINING_BATCH_SIZE, epochs=2, verbose=1,
						validation_data=validation_batch_generator,
						validation_steps=len(valid_stamps) // TRAINING_BATCH_SIZE,
						use_multiprocessing=False)

# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.savefig('acc_model20.png')

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.savefig('loss_model20.png')
