from tkinter import *
from PIL import ImageTk, Image
import os
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
        self.top_frame = Frame(root, width=960, height=480)
        self.top_frame.grid(row=0, column=0)
        self.bottom_frame = Frame(root, width=960, height=120)
        self.bottom_frame.grid(row=1, column = 0)
        self.data_dir = data_dir
        self.photo = None
        self.mask = None
        self.mask_label = None
        self.history = []
        self.timestamp = '20180419000200'
        self.load_images()
        self.layout()

    def load_images(self):
        self.photo = ImageTk.PhotoImage(Image.open(timestamp_to_photo_path(self.data_dir, self.timestamp)))
        self.mask = imread(timestamp_to_tsi_mask_path(self.data_dir, self.timestamp))[:, :, :3]

    def layout(self):
        # Photo
        photo_label = Label(self.top_frame, image=self.photo)
        photo_label.image = self.photo  # This seems redundant with the named argument above, but both seem to be necessary
        photo_label.pack(side='left')
        # Mask
        mask_image = ImageTk.PhotoImage(Image.fromarray(self.mask))
        self.mask_label = Label(self.top_frame, image=mask_image)
        self.mask_label.image = mask_image
        self.mask_label.pack(side='right')
        self.mask_label.bind("<Button>", self.click)
        # Buttons
        Button(self.bottom_frame, text="Undo", command=self.undo).grid(row=0, column=0)
        Button(self.bottom_frame, text="Save", command=self.save).grid(row=0, column=1)

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
        path = os.path.expanduser(timestamp_to_tsi_mask_no_glare_path('~/Desktop', self.timestamp))
        os.makedirs(path[:path.rfind('/')], exist_ok=True)
        imsave(path, self.mask, check_contrast=False)


if __name__ == "__main__":
    root = Tk()
    app = ManualGlareRemover(root, '../test_data')
    root.mainloop()
