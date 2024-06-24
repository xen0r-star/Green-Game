from tkinter import *
from PIL import Image, ImageTk



class custom_Image(Frame):
    """
        Classe pour un widget d'image personnalisé. C'est un label dans lequel on peut mettre une image.
        Cela permet de ne pas répéter plusieurs fois ce code, souvent utilisé pour afficher des images
        dans le programme.
    """
    
    def __init__(self, parent, image, text="", font = None, fg = None, bg = None, width = 100, height = 100, sticky=None, wraplength=None, rowspan=1, columnspan=1 , column=0, row=0, padx=0, pady=0, ipadx=0, ipady=0, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.parent = parent

        self.image = image
        self.width, self.height = width, height
        self.text, self.font, self.wraplength = text, font, wraplength

        self.bg, self.fg = bg, fg
        self.column, self.row = column, row
        self.padx, self.pady = padx, pady
        self.ipadx, self.ipady = ipadx, ipady
        self.rowspan, self.columnspan = rowspan, columnspan
        self.sticky = sticky

        self.create_image()

    def create_image(self):
        photo = ImageTk.PhotoImage(
            Image.open(self.image).resize((self.width, self.height), Image.LANCZOS)
        )
        self.custom_Image = Label(self.parent, image=photo, text=self.text, compound="center", font=self.font, fg=self.fg, bg=self.bg, wraplength=self.wraplength)
        self.custom_Image.image = photo
        self.custom_Image.grid(column=self.column, row=self.row, 
                               rowspan=self.rowspan, columnspan=self.columnspan,
                               padx=self.padx, pady=self.pady, 
                               ipadx=self.ipadx, ipady=self.ipady,
                               sticky=self.sticky)