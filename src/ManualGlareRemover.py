from tkinter import *
from PIL import ImageTk, Image
from config import *
from utils_timestamp import *
from skimage.io import imsave, imread


class ManualGlareRemover:
    """
    Allows a user to interactively remove patches of glare (incorrectly classified as clouds) from TSI masks to
    provide improved training data.
    """
    def __init__(self, root, data_dir):
        self.root = root
        self.data_dir = data_dir
        self.load_images()

    def load_images(self):
        timestamp = '20180419000200'
        self.root.geometry('960x480')
        photo = ImageTk.PhotoImage(Image.open(timestamp_to_photo_path(self.data_dir, timestamp)))
        photo_label = Label(self.root, image=photo)
        photo_label.image = photo  # This seems redundant with the named argument above, but both seem to be necessary
        photo_label.pack(side='left')
        mask_image = ImageTk.PhotoImage(Image.open(timestamp_to_tsi_mask_path(self.data_dir, timestamp)))
        mask_label = Label(self.root, image=mask_image)
        mask_label.image = mask_image  # This seems redundant with the named argument above, but both seem to be necessary
        mask_label.pack(side='right')
        mask_label.bind("<Button>", self.click)
        self.mask = imread(timestamp_to_tsi_mask_path(self.data_dir, timestamp))[:, :, :3]

    def click(self, event):
        print(f'x={event.x}, y={event.y}')
        print(self.mask[event.y, event.x, :])  # Note the inversion because the numpy array is r, c rather than x, y

if __name__ == "__main__":
    root = Tk()
    app = ManualGlareRemover(root, '/home/drake/PycharmProjects/sky/test_data')
    root.mainloop()
