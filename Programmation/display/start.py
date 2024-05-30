from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import cv2
import random
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

paths = Path(__file__).parent.resolve()



class displayStart(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.canvas_width = 604
        self.canvas_height = 340
        self.canvas_border = 6

        self.video_source = [str(paths / "../assets/video/Car 1.mp4"), str(paths / "../assets/video/Car 2.mp4")]

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.addComponents()

        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)


    def addComponents(self):
        custom_Image(self, image=paths / "../assets/Background.png", bg=self.master.color_background, width=700, height=700, column=0, row=0, rowspan=3)

        self.canvas = Canvas(self, height=self.canvas_height, width=self.canvas_width, bg=self.master.color_second, highlightthickness=self.canvas_border, highlightbackground="white")
        self.canvas.grid(column=0, row=0, padx=10, pady=10)
        
        self.cap = cv2.VideoCapture(random.choice(self.video_source))
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.ratio = min(self.canvas_width / self.video_width, self.canvas_height / self.video_height)
        
        custom_Button(self, 
                        command=self.master.startGame, 
                        text="J O U E R", font=font.Font(size=30, weight="bold"),
                        image=paths / "../assets/Button1.png",
                        height=90, width=412, 
                        bg=self.master.color_background, fg=self.master.color_text, 
                        column=0, row=1, pady=(10,0), ipadx=5, ipady=2)

        custom_Button(self, 
                        command=self.master.quit, 
                        text="Q U I T T E R", font=font.Font(size=15, weight="bold"),
                        image=paths / "../assets/Button1.png",
                        height=50, width=230, 
                        bg=self.master.color_background, fg=self.master.color_text, 
                        column=0, row=2, pady=(0, 50), ipadx=5, ipady=2)
        
        self.update_frame()
    

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            new_width = int(self.video_width * self.ratio) + self.canvas_border * 2
            new_height = int(self.video_height * self.ratio) + self.canvas_border * 2 + 1
            resized_frame = cv2.resize(frame, (new_width, new_height))

            frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

            self.canvas.delete("all")
            self.canvas.create_image((self.canvas_width - new_width) // 2, (self.canvas_height - new_height) // 2, anchor=NW, image=self.photo)

            self.after(33, self.update_frame)
        else:
            self.cap.release()
            self.cap = cv2.VideoCapture(random.choice(self.video_source))
            self.update_frame()