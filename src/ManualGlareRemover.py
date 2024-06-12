import tkinter.messagebox
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
        self.mask_image = None
        self.photo_canvas = None
        self.mask_canvas = None
        self.mask_canvas_image_id = None
        self.remove_region_label = None
        self.remove_thin_region_label = None
        self.remove_circular_region_label = None
        self.remove_all_thin_button = None
        self.remove_all_button = None
        self.undo_button = None
        self.prev_button = None
        self.next_button = None
        self.save_button = None
        self.drag_ends = None
        self.histories = None
        self.timestamps_to_process = []
        self.timestamp_index = 0  # Index into timestamps_to_process
        self.timestamp = None
        self.choose_timestamps()
        self.download_images()
        self.load_images()
        self.layout()

    def choose_timestamps(self):
        # TODO Fail more gracefully when there are no images left to process at beginning of a run
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
            if (stamp.endswith('000') or stamp.endswith('500')) and stamp not in deglared_stamps:
                self.timestamps_to_process.append(stamp)
                i += 1
        self.histories = [[] for _ in self.timestamps_to_process]

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
        if self.histories[self.timestamp_index - 1]:
            self.mask = self.histories[self.timestamp_index - 1].pop()
        else:
            self.mask = imread(timestamp_to_tsi_mask_path(self.data_dir, self.timestamp))[:, :, :3]

    def layout(self):
        # Clear out existing elements
        if self.mask_canvas:  # Either all or none of them should exist, so checking one suffices
            self.photo_canvas.destroy()
            self.mask_canvas.destroy()
            self.remove_region_label.destroy()
            self.remove_thin_region_label.destroy()
            self.remove_circular_region_label.destroy()
            self.undo_button.destroy()
            self.remove_all_thin_button.destroy()
            self.remove_all_button.destroy()
            self.prev_button.destroy()
            self.next_button.destroy()
            self.save_button.destroy()
        # Title
        # Note that, since load_images has been called, self.timestamp_index holds the 0-based index
        # of the NEXT image to be edited. We display that anyway as it is also the 1-based index
        # of the image currently being edited.
        self.root.title(f'Glare Editor: {self.timestamp} ({self.timestamp_index}/{len(self.timestamps_to_process)})')
        # # Frames
        # upper_frame = Frame(self.root)
        # upper_frame.grid(row=0, column=0)
        # lower_frame = Frame(self.root)
        # Photo
        self.photo_canvas = Canvas(self.top_frame, width=480, height=480)
        self.photo_canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.photo_canvas.pack(side='left')
        # Mask
        self.mask_image = ImageTk.PhotoImage(Image.fromarray(self.mask))
        self.mask_canvas = Canvas(self.top_frame, width=480, height=480)
        self.mask_canvas_image_id = self.mask_canvas.create_image(0, 0, anchor='nw', image=self.mask_image)
        self.mask_canvas.pack(side='right')
        self.mask_canvas.bind('<Button-1>', self.click)
        # It seems like the right button is Button-2 on a Mac, but Button-3 on Ubuntu
        self.mask_canvas.bind('<Button-2>', self.right_click)
        self.mask_canvas.bind('<Button-3>', self.right_click)
        self.mask_canvas.bind('<Shift-ButtonPress-1>', self.start_drag)
        self.mask_canvas.bind('<Shift-B1-Motion>', self.drag)
        self.mask_canvas.bind('<B1-Motion>', self.drag)
        self.mask_canvas.bind('<Shift-ButtonRelease-1>', self.finish_drag)
        self.mask_canvas.bind('<ButtonRelease-1>', self.finish_drag)
        self.root.bind('<Key>', self.key_pressed)
        # Labels
        self.remove_region_label = Label(self.bottom_frame, text="Remove\nthick+thin region\n(click)")
        self.remove_region_label.grid(row=0, column=0, padx=10)
        self.remove_thin_region_label = Label(self.bottom_frame, text="Remove\nthin region\n(right click)")
        self.remove_thin_region_label.grid(row=0, column=1, padx=10)
        self.remove_circular_region_label = Label(self.bottom_frame, text="Remove\ncircular region\n(shift drag)")
        self.remove_circular_region_label.grid(row=0, column=2, padx=10)
        # Buttons
        self.remove_all_thin_button = Button(self.bottom_frame, text="Remove\nall thin clouds\n(tab)", command=self.remove_all_thin_clouds)
        self.remove_all_thin_button.grid(row=0, column=3)
        self.remove_all_button = Button(self.bottom_frame, text="Remove\nall clouds\n(space)", command=self.remove_all_clouds)
        self.remove_all_button.grid(row=0, column=4)
        self.undo_button = Button(self.bottom_frame, text="Undo\n\n(backspace)", command=self.undo)
        self.undo_button.grid(row=0, column=5)
        self.prev_button = Button(self.bottom_frame, text="Prev\n\n(<)", command=self.prev)
        self.prev_button.grid(row=0, column=6)
        if self.timestamp_index == 1:
            self.prev_button['state'] = DISABLED
        self.next_button = Button(self.bottom_frame, text="Next\n\n(>)", command=self.next)
        self.next_button.grid(row=0, column=7)
        self.save_button = Button(self.bottom_frame, text="Save\nall\n(enter)", command=self.save)
        self.save_button.grid(row=0, column=8)
        if self.timestamp_index == len(self.timestamps_to_process):
            self.next_button['state'] = DISABLED
        else:
            self.save_button['state'] = DISABLED

    def update_mask(self):
        self.mask_image = ImageTk.PhotoImage(Image.fromarray(self.mask))
        self.mask_canvas.itemconfig(self.mask_canvas_image_id, image=self.mask_image)

    def key_pressed(self, event):
        if event.keysym == 'Tab':
            self.remove_all_thin_clouds()
        elif event.keysym == 'space':
            self.remove_all_clouds()
        elif event.keysym == 'comma':
            if self.prev_button['state'] == NORMAL:
                self.prev()
        elif event.keysym == 'period':
            if self.next_button['state'] == NORMAL:
                self.next()
        elif event.keysym == 'Return':
            if self.next_button['state'] == DISABLED:  # Because you're looking at the last image
                self.save()
        elif event.keysym == 'BackSpace':
            self.undo()
        elif event.keysym in ['Shift_L', 'Shift_R']:
            pass  # Ignore these, are they are expected when shift-dragging
        else:
            print('Unknown key pressed: <' + event.keysym + '>')

    def click(self, event):
        label = rgb_mask_to_label(self.mask)  # This is a label in the sense of utils_timestamp, not tkinter
        if label[event.y, event.x] in (1, 2, 3):  # If the point is blue, gray, or white
            self.histories[self.timestamp_index - 1].append(self.mask)
            # Before the flood fill, set the point in question to white, so that a tolerance of 1 also catches gray.
            # Otherwise, clicking on a gray pixel would put blue within the tolerance, making the flood fill far too
            # large.
            label[event.y, event.x] = 3  # The number 3 indicates white
            label = flood_fill(label,
                               (event.y, event.x),
                               1,  # Blue
                               tolerance=1,
                               footprint=ManualGlareRemover.FOOTPRINT)
            self.mask = label_to_rgb_mask(label)
            self.update_mask()

    def right_click(self, event):
        label = rgb_mask_to_label(self.mask)  # This is a label in the sense of utils_timestamp, not tkinter
        if label[event.y, event.x] == 2:  # If the point is gray
            self.histories[self.timestamp_index - 1].append(self.mask)
            label = flood_fill(label,
                               (event.y, event.x),
                               1,  # Blue
                               tolerance=0.5,
                               footprint=ManualGlareRemover.FOOTPRINT)
            self.mask = label_to_rgb_mask(label)
            self.update_mask()

    def start_drag(self, event):
        self.drag_ends = [(event.x, event.y), None]

    def drag(self, event):
        if not self.drag_ends:
            return  # User pressed shift after beginning drag; do nothing
        self.drag_ends[1] = (event.x, event.y)
        self.mask_canvas.delete('circle')
        [(x1, y1), (x2, y2)] = self.drag_ends
        cx, cy = ((x1 + x2)/2, (y1+y2)/2)
        r = (((x1 - cx) ** 2) + ((y1 - cy) ** 2)) ** 0.5
        circle = self.mask_canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline='red')
        self.mask_canvas.itemconfig(circle, tags='circle')
        return (cx, cy), r

    def finish_drag(self, event):
        if not self.drag_ends:
            return  # User pressed shift after beginning drag; do nothing
        center, radius = self.drag(event)
        # Process the drag
        self.histories[self.timestamp_index - 1].append(self.mask)
        self.mask = self.mask.copy()
        remove_all_clouds_within_circle(self.mask, center, radius)  # This destructively modifies its arguments, hence the copy
        self.update_mask()
        # Delete the circle
        self.mask_canvas.delete('circle')
        self.drag_ends = None

    def remove_all_clouds(self):
        self.histories[self.timestamp_index - 1].append(self.mask)
        self.mask = self.mask.copy()
        remove_all_clouds(self.mask)  # This destructively modifies its arguments, hence the copy
        self.update_mask()

    def remove_all_thin_clouds(self):
        self.histories[self.timestamp_index - 1].append(self.mask)
        self.mask = self.mask.copy()
        remove_all_thin_clouds(self.mask)  # This destructively modifies its arguments, hence the copy
        self.update_mask()

    def undo(self):
        if self.histories[self.timestamp_index - 1]:
            self.mask = self.histories[self.timestamp_index - 1].pop()
            self.update_mask()

    def prev(self):
        history = self.histories[self.timestamp_index - 1]
        if (not history) or not (history[-1] == self.mask).all():
            history.append(self.mask)
        self.timestamp_index -= 2
        self.next()

    def next(self):
        history = self.histories[self.timestamp_index - 1]
        if (not history) or not (history[-1] == self.mask).all():
            history.append(self.mask)
        path = timestamp_to_tsi_mask_no_glare_path(self.data_dir, self.timestamp)
        os.makedirs(path[:path.rfind('/')], exist_ok=True)
        imsave(path, self.mask, check_contrast=False)
        self.load_images()
        self.layout()

    def save(self):
        path = timestamp_to_tsi_mask_no_glare_path(self.data_dir, self.timestamp)
        os.makedirs(path[:path.rfind('/')], exist_ok=True)
        imsave(path, self.mask, check_contrast=False)
        if tkinter.messagebox.askyesno('Upload', 'Upload all images and quit?'):
            print('Done -- just need to upload')
            self.upload_files()
            self.root.destroy()

    def upload_files(self):
        print('NOT UPLOADING ANY FILES WHILE TESTING NEW FEATURES')
        # user = os.environ.get('user')
        # password = os.environ.get('password')
        # with pysftp.Connection(host='mayo.blt.lclark.edu', username=user, password=password) as connection:
        #     for timestamp in self.timestamps_to_process:
        #         print("Uploading " + timestamp)
        #         tsi_mask_path = timestamp_to_tsi_mask_no_glare_path(self.data_dir, timestamp)
        #         remote_path = timestamp_to_tsi_mask_no_glare_path(DATA_DIR, timestamp)
        #         connection.makedirs(remote_path[:remote_path.rfind('/')])
        #         connection.put(tsi_mask_path, remote_path)
        #     print("Uploading revised list of deglared timestamps")
        #     with open(self.data_dir + '/typical_training_deglared_timestamps', 'a') as f:
        #         for timestamp in self.timestamps_to_process:
        #             f.write(timestamp + '\n')
        #     connection.put(self.data_dir + '/typical_training_deglared_timestamps',
        #                    DATA_DIR + '/typical_training_deglared_timestamps')


if __name__ == "__main__":
    root = Tk()
    app = ManualGlareRemover(root, os.path.expanduser('~/Desktop'))
    root.mainloop()
