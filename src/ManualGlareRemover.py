from tkinter import *
from PIL import ImageTk, Image
from config import *
from utils_timestamp import *
from utils_image import *
from skimage.io import imsave, imread
from skimage.morphology import flood_fill


class ManualGlareRemover:
    """
    Allows a user to interactively remove patches of glare (incorrectly classified as clouds) from TSI masks to
    provide improved training data.
    """

    FOOTPRINT = np.ones((9, 9))  # Neighborhood for flood fill

    def __init__(self, root, data_dir):
        self.root = root
        self.root.title('Glare Editor')
        self.data_dir = data_dir
        self.mask = None
        self.mask_label = None
        self.load_images()

    def load_images(self):
        timestamp = '20180419000200'
        self.root.geometry('960x480')
        photo = ImageTk.PhotoImage(Image.open(timestamp_to_photo_path(self.data_dir, timestamp)))
        photo_label = Label(self.root, image=photo)
        photo_label.image = photo  # This seems redundant with the named argument above, but both seem to be necessary
        photo_label.pack(side='left')
        self.mask = imread(timestamp_to_tsi_mask_path(self.data_dir, timestamp))[:, :, :3]
        mask_image = ImageTk.PhotoImage(Image.fromarray(self.mask))
        self.mask_label = Label(self.root, image=mask_image)
        self.mask_label.image = mask_image  # This seems redundant with the named argument above, but both seem to be necessary
        self.mask_label.pack(side='right')
        self.mask_label.bind("<Button>", self.click)

    def click(self, event):
        label = rgb_mask_to_label(self.mask)
        if label[event.y, event.x] in (1, 2, 3):  # If the point is blue, gray, or white
            # Before the flood fill, set the point in question to white, so that a tolerance of 0.75 also catches gray.
            # Otherwise, clicking on a gray pixel would put blue within the tolerance, making the flood fill far too
            # large.
            label[event.y, event.x] = 3  # The number 3 indicates white
            flood_fill(label,
                       (event.y, event.x),
                       1,  # Blue
                       tolerance=1,
                       footprint=ManualGlareRemover.FOOTPRINT,
                       in_place=True)
            self.mask = label_to_rgb_mask(label)
            image = ImageTk.PhotoImage(Image.fromarray(self.mask))
            self.mask_label.configure(image=image)
            self.mask_label.image = image


if __name__ == "__main__":
    root = Tk()
    app = ManualGlareRemover(root, '/home/drake/PycharmProjects/sky/test_data')
    root.mainloop()
