from BatchGenerator import *

# TODO This repeats code from run_train
stamps = pd.read_csv('../test_data/tiny_data.csv', converters={'timestamp_utc': str}, usecols=['timestamp_utc'])
stamps = stamps['timestamp_utc'].tolist()
train_stamps = stamps[:96]
val_stamps = stamps[96:192]

model = keras.models.load_model('network.h5')

val_gen = BatchGenerator(val_stamps, '../test_data')
val_preds = model.predict(val_gen)

def display_mask(i):
    """Quick utility to display a model's prediction."""
    mask = np.argmax(val_preds[i], axis=-1)
    mask = np.expand_dims(mask, axis=-1)
    plt.imshow(mask)

display_mask(0)
