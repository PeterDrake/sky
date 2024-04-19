from tkinter import *
from PIL import ImageTk, Image
import os
from utils_timestamp import *
from utils_image import *
from skimage.io import imsave, imread
from skimage.morphology import flood_fill
from dotenv import load_dotenv
import pysftp
from config import *


class ManualGlareRemover:
    """
    Allows a user to interactively remove patches of glare (incorrectly classified as clouds) from TSI masks to
    provide improved training data.
    """

    FOOTPRINT = np.ones((9, 9))  # Neighborhood for flood fill

    IMAGES_PER_SESSION = 3

    def __init__(self, root, data_dir):
        self.root = root
        self.root.title('Glare Editor')
        self.top_frame = Frame(root, width=960, height=480)
        self.top_frame.grid(row=0, column=0)
        self.bottom_frame = Frame(root, width=960, height=120)
        self.bottom_frame.grid(row=1, column = 0)
        self.data_dir = data_dir
        self.photo = None
        self.mask = None
        self.photo_label = None
        self.mask_label = None
        self.undo_button = None
        self.save_next_button = None
        self.history = []
        self.timestamps_to_process = []
        self.timestamp_index = 0  # Index into timestamps_to_process
        self.timestamp = None
        self.choose_timestamps()
        self.download_images()
        self.load_images()
        self.layout()

    def choose_timestamps(self):
        load_dotenv()
        user = os.environ.get('user')
        password = os.environ.get('password')
        all_stamps_path = self.data_dir + '/typical_training_timestamps'
        deglared_stamps_path = self.data_dir + '/typical_training_deglared_timestamps'
        with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
            print('Pulling typical timestamps from BLT')
            connection.get(DATA_DIR + '/typical_training_timestamps',
                           all_stamps_path)
            print('Pulling already deglared timestamps')
            try:
                connection.get(DATA_DIR + '/typical_training_deglared_timestamps', deglared_stamps_path)
            except FileNotFoundError:
                print("Deglared list doesn't exist yet -- creating it")
                # connection.get has already created an empty file in this case
        all_stamps = []
        deglared_stamps = set()
        with open(all_stamps_path, 'r') as f:
            for line in f.readlines():
                all_stamps.append(line.strip())
        with open(deglared_stamps_path, 'r') as f:
            for line in f.readlines():
                deglared_stamps.add(line.strip())
        m = len(deglared_stamps)
        n = len(all_stamps)
        print(f'{m}/{n} images already processed, {n - m} to go')
        self.timestamps_to_process = []
        i = 0
        for stamp in all_stamps:
            if i == self.IMAGES_PER_SESSION:
                break
            if stamp not in deglared_stamps:
                self.timestamps_to_process.append(stamp)
                i += 1

    def download_images(self):
        user = os.environ.get('user')
        password = os.environ.get('password')
        with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
            for timestamp in self.timestamps_to_process:
                print(timestamp)
                photo_path = timestamp_to_photo_path(self.data_dir, timestamp)
                os.makedirs(photo_path[:photo_path.rfind('/')], exist_ok=True)
                connection.get(timestamp_to_photo_path(DATA_DIR, timestamp), photo_path)
                tsi_mask_path = timestamp_to_tsi_mask_path(self.data_dir, timestamp)
                os.makedirs(tsi_mask_path[:tsi_mask_path.rfind('/')], exist_ok=True)
                connection.get(timestamp_to_tsi_mask_path(DATA_DIR, timestamp), tsi_mask_path)


    def load_images(self):
        self.timestamp = self.timestamps_to_process[self.timestamp_index]
        self.timestamp_index += 1
        self.photo = ImageTk.PhotoImage(Image.open(timestamp_to_photo_path(self.data_dir, self.timestamp)))
        self.mask = imread(timestamp_to_tsi_mask_path(self.data_dir, self.timestamp))[:, :, :3]

    def layout(self):
        # Clear out existing elements
        if self.mask_label:  # Either all or none of them should exist, so checking one suffices
            self.photo_label.destroy()
            self.mask_label.destroy()
            self.undo_button.destroy()
            self.save_next_button.destroy()
        # Photo
        self.photo_label = Label(self.top_frame, image=self.photo)
        self.photo_label.image = self.photo  # This seems redundant with the named argument above, but both seem to be necessary
        self.photo_label.pack(side='left')
        # Mask
        mask_image = ImageTk.PhotoImage(Image.fromarray(self.mask))
        self.mask_label = Label(self.top_frame, image=mask_image)
        self.mask_label.image = mask_image
        self.mask_label.pack(side='right')
        self.mask_label.bind("<Button>", self.click)
        # Buttons
        self.undo_button = Button(self.bottom_frame, text="Undo", command=self.undo)
        self.undo_button.grid(row=0, column=0)
        self.save_next_button = Button(self.bottom_frame, text="Save/Next", command=self.save)
        self.save_next_button.grid(row=0, column=1)

    def update_mask(self):
        image = ImageTk.PhotoImage(Image.fromarray(self.mask))
        self.mask_label.configure(image=image)
        self.mask_label.image = image

    def click(self, event):
        label = rgb_mask_to_label(self.mask)  # This is a label in the sense of utils_timestamp, not tkinter
        if label[event.y, event.x] in (1, 2, 3):  # If the point is blue, gray, or white
            # Before the flood fill, set the point in question to white, so that a tolerance of 0.75 also catches gray.
            # Otherwise, clicking on a gray pixel would put blue within the tolerance, making the flood fill far too
            # large.
            self.history.append(self.mask)
            label[event.y, event.x] = 3  # The number 3 indicates white
            label = flood_fill(label,
                               (event.y, event.x),
                               1,  # Blue
                               tolerance=1,
                               footprint=ManualGlareRemover.FOOTPRINT)
            self.mask = label_to_rgb_mask(label)
            self.update_mask()

    def undo(self):
        if self.history:
            self.mask = self.history.pop()
            self.update_mask()

    def save(self):
        path = timestamp_to_tsi_mask_no_glare_path(self.data_dir, self.timestamp)
        os.makedirs(path[:path.rfind('/')], exist_ok=True)
        imsave(path, self.mask, check_contrast=False)
        if self.timestamp_index < len(self.timestamps_to_process):  # If there are any left, move on to the next one
            self.load_images()
            self.layout()
        else:  # Done -- upload the results
            print('Done -- just need to upload')
            self.upload_files()
            self.root.destroy()

    def upload_files(self):
        user = os.environ.get('user')
        password = os.environ.get('password')
        with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
            for timestamp in self.timestamps_to_process:
                print("Uploading " + timestamp)
                tsi_mask_path = timestamp_to_tsi_mask_path(self.data_dir, timestamp)
                remote_path = timestamp_to_tsi_mask_no_glare_path(DATA_DIR, timestamp)
                connection.makedirs(remote_path[:remote_path.rfind('/')])
                connection.put(tsi_mask_path, remote_path)
            print("Uploading revised list of deglared timestamps")
            with open(self.data_dir + '/typical_training_deglared_timestamps', 'a') as f:
                for timestamp in self.timestamps_to_process:
                    f.write(timestamp + '\n')
            connection.put(self.data_dir + '/typical_training_deglared_timestamps',
                           DATA_DIR + '/typical_training_deglared_timestamps')


if __name__ == "__main__":
    root = Tk()
    app = ManualGlareRemover(root, os.path.expanduser('~/Desktop'))
    root.mainloop()
