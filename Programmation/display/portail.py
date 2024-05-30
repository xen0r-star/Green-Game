from tkinter import *
from tkinter import font
from pathlib import Path
from PIL import Image, ImageTk

from widgets.Image import custom_Image
from widgets.Button import custom_Button

paths = Path(__file__).parent.resolve()



class displayPortail(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")
        self.addComponents()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def addComponents(self):
        custom_Image(self, image=paths / "../assets/Background.png", 
                     bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, columnspan=2, row=0, rowspan=3)


        self.navbar = Frame(self)
        self.navbar.grid(column=0, columnspan=2, row=0)

        custom_Image(self.navbar, image=paths / "../assets/portail/Header_Portail.png", 
                     bg=self.master.color_background, 
                     width=571, height=82, 
                     column=0, columnspan=2, row=0)
        
        custom_Button(self.navbar, image=paths / "../assets/Home.png",
                      command=self.master.startGame,
                      bg=self.master.color_second,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(0, 20))


        self.frame = Frame(self)
        self.frame.grid(column=0, columnspan=2, row=1)

        custom_Image(self.frame, image=paths / "../assets/Frame3.png", 
                     bg=self.master.color_background, 
                     height=274, width=571, 
                     column=0, row=0, rowspan=3)

        fontStyle = font.Font(size=25, weight="bold")
        self.text = Label(self.frame, text="Saisie le code a l'arrier du portail pour te connecter", wraplength=487, 
                          bg=self.master.color_second, fg=self.master.color_text, font=fontStyle)
        self.text.grid(column=0, row=0, pady=0)

        fontStyle = font.Font(size=27, weight="bold")
        self.entry = Text(self.frame, bg=self.master.color_third, 
                          width=20, height=1, 
                          font=fontStyle, fg=self.master.color_text, 
                          highlightthickness=4, highlightbackground="white", highlightcolor="white")
        self.entry.grid(column=0, row=1, ipadx=5)
        self.center_text(None)
        self.entry.bind("<KeyRelease>", self.center_text)

        photo = ImageTk.PhotoImage(
            Image.open(paths / "../assets/portail/Connexion.png").resize((303, 51), Image.LANCZOS)
        )
        self.button_connexion = Button(self.frame, command=lambda: self.master.connexionPortail(self.entry.get(1.0, END)), image=photo, 
                                    bg=self.master.color_second,
                                    cursor="hand2", compound=CENTER, 
                                    bd=0, highlightthickness=0, highlightbackground="white", 
                                    activebackground=self.master.color_second)
        self.button_connexion.image = photo
        self.button_connexion.grid(column=0, row=2, ipadx=5, ipady=2)


    def center_text(self, event):
        self.entry.tag_configure("center", justify='center')
        self.entry.tag_add("center", "1.0", "end")