# From https://www.makeuseof.com/python-paint-application-build/

import tkinter as tk
from tkinter.ttk import Scale
from tkinter import colorchooser, filedialog, messagebox
import PIL.ImageGrab as ImageGrab


class DrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids' Paint App")
        self.root.attributes("-fullscreen", True)
        self.pointer = "black"
        self.erase = "white"
        self.setup_widgets()

    def setup_widgets(self):
        self.title_label = tk.Label(
            self.root,
            text="Kids' Paint App",
            font=("Comic Sans MS", 30),
            bg="lightblue",
            fg="purple",
        )
        self.title_label.pack(fill=tk.X, pady=10)
        self.color_frame = tk.LabelFrame(
            self.root,
            text="Colors",
            font=("Comic Sans MS", 15),
            bd=5,
            relief=tk.RIDGE,
            bg="white",
        )
        # Increased width
        self.color_frame.place(x=10, y=80, width=130, height=180)
        colors = [
            "blue",
            "red",
            "green",
            "orange",
            "violet",
            "black",
            "yellow",
            "purple",
            "pink",
            "gold",
            "brown",
            "indigo",
        ]
        i, j = 0, 0
        for color in colors:
            tk.Button(
                self.color_frame,
                bg=color,
                bd=2,
                relief=tk.RIDGE,
                width=1,  # Was 3
                command=lambda col=color: self.select_color(col),
            ).grid(row=i, column=j, padx=2, pady=2)
            i += 1
            if i == 4:
                i = 0
                j += 1  # Fixed error; was j = 1
        self.eraser_btn = tk.Button(
            self.root,
            text="Eraser",
            bd=4,
            bg="white",
            command=self.eraser,
            width=9,
            relief=tk.RIDGE,
            font=("Comic Sans MS", 12),
        )
        self.eraser_btn.place(x=10, y=310)
        self.clear_screen_btn = tk.Button(
            self.root,
            text="Clear Screen",
            bd=4,
            bg="white",
            command=self.clear_screen,
            width=12,
            relief=tk.RIDGE,
            font=("Comic Sans MS", 12),
        )
        self.clear_screen_btn.place(x=10, y=370)
        self.save_as_btn = tk.Button(
            self.root,
            text="Save Drawing",
            bd=4,
            bg="white",
            command=self.save_as,
            width=12,
            relief=tk.RIDGE,
            font=("Comic Sans MS", 12),
        )
        self.save_as_btn.place(x=10, y=430)
        self.bg_btn = tk.Button(
            self.root,
            text="Background",
            bd=4,
            bg="white",
            command=self.canvas_color,
            width=12,
            relief=tk.RIDGE,
            font=("Comic Sans MS", 12),
        )
        self.bg_btn.place(x=10, y=490)
        self.pointer_frame = tk.LabelFrame(
            self.root,
            text="Size",
            bd=5,
            bg="white",
            font=("Comic Sans MS", 15, "bold"),
            relief=tk.RIDGE,
        )
        self.pointer_frame.place(x=10, y=580, height=150, width=70)
        self.pointer_size = Scale(
            self.pointer_frame, orient=tk.VERTICAL, from_=48, to=1, length=120
        )
        self.pointer_size.set(1)
        self.pointer_size.grid(row=0, column=1, padx=15)
        self.canvas = tk.Canvas(
            self.root, bg="white", bd=5, relief=tk.GROOVE, height=650, width=1300
        )
        self.canvas.place(x=160, y=120, anchor="nw")
        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        self.canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            fill=self.pointer,
            outline=self.pointer,
            width=self.pointer_size.get(),
        )

    def select_color(self, col):
        self.pointer = col

    def eraser(self):
        self.pointer = self.erase

    def clear_screen(self):
        self.canvas.delete("all")

    def canvas_color(self):
        color = colorchooser.askcolor()
        if color:
            self.canvas.configure(background=color[1])
            self.erase = color[1]

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg", filetypes=[("Image files", "*.jpg")]
        )
        if file_path:
            try:
                y = 148
                x = 200
                y1 = 978
                x1 = 1840
                ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
                messagebox.showinfo("Save Drawing", "Image file saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the image file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawApp(root)
    root.mainloop()
