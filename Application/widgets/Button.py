from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

class custom_Button(Frame):
    def __init__(self, parent, image, bg, fg, width, height, command, text="Click here", column=0, row=0, padx=0, pady=0, ipadx=0, ipady=0, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.parent = parent

        self.image = image
        self.width, self.height = width, height
        self.text = text
        self.command = command

        self.bg, self.fg = bg, fg
        self.column, self.row = column, row
        self.padx, self.pady = padx, pady
        self.ipadx, self.ipady = ipadx, ipady

        self.create_buttons()

    def create_buttons(self):
        def buttonClicked():
            if self.command and callable(self.command):
                self.command()

        fontStyle = font.Font(size=25, weight="bold")
        
        photo = ImageTk.PhotoImage(
            Image.open(self.image).resize((self.width, self.height), Image.LANCZOS)
        )
        button = Button(self.parent, command=buttonClicked, text=self.text, fg=self.fg, font=fontStyle, image=photo, bg=self.bg, cursor="hand2", compound=CENTER, bd=0, highlightthickness=0, highlightbackground="white", activebackground=self.bg, activeforeground=self.fg)
        button.image = photo

        button.grid(column=self.column, row=self.row, padx=self.padx, pady=self.pady, ipadx=self.ipadx, ipady=self.ipady)
    