from tkinter import *
from tkinter import font as fontstyle
from PIL import Image, ImageTk



class custom_Button(Frame):
    """
    class pour un widget custom bouton, c'est un bouton ou on va mettre une image dedans
    sa permets de ne pas devoir refaire plusieur fois se code qui est tres souvent utiliser pour mettre des bouton des apparence différente dans le programme
    """

    def __init__(self, parent, image, bg = None, fg = None, width = 100, height = 100, command = None, text="", font=None, sticky=None, rowspan=1, columnspan=1 , column=0, row=0, padx=0, pady=0, ipadx=0, ipady=0, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.parent = parent

        self.image = image
        self.width, self.height = width, height
        self.text = text
        if font == None:
            self.font = fontstyle.Font(size=25, weight="bold")
        else:
            self.font = font
    
        self.command = command

        self.bg, self.fg = bg, fg
        self.column, self.row = column, row
        self.padx, self.pady = padx, pady
        self.ipadx, self.ipady = ipadx, ipady
        self.rowspan, self.columnspan = rowspan, columnspan
        self.sticky = sticky

        self.create_buttons()

    def create_buttons(self):
        def buttonClicked():
            if self.command and callable(self.command):  # callable => savoir si une variable est appelable 
                self.command()
        
        photo = ImageTk.PhotoImage(
            Image.open(self.image).resize((self.width, self.height), Image.LANCZOS)
        )
        button = Button(self.parent, command=buttonClicked, text=self.text, image=photo, 
                        bg=self.bg, fg=self.fg, font=self.font, 
                        cursor="hand2", compound=CENTER, 
                        bd=0, highlightthickness=0, highlightbackground="white", 
                        activebackground=self.bg, activeforeground=self.fg)
        button.image = photo

        button.grid(column=self.column, row=self.row, 
                    rowspan=self.rowspan, columnspan=self.columnspan,
                    padx=self.padx, pady=self.pady, 
                    ipadx=self.ipadx, ipady=self.ipady,
                    sticky=self.sticky)
    