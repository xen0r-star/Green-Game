from tkinter import *
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

paths = Path(__file__).parent.resolve()



class displayMenu(Frame):
    """
        Classe de l'écran du menu (solo, duo, portail)
    """

    def __init__(self, master):
        super().__init__(master)
        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.master.color_background = "#BFEA7C"

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.addComponents()


    def addComponents(self):
        custom_Image(self, image=paths / "../assets/Background.png", bg=self.master.color_background, width=700, height=700, column=0, columnspan=2, row=0, rowspan=3)

        "------ Barre de navigation -------------------------------------------------------------------"
        self.navbar = Frame(self)
        self.navbar.grid(column=0, columnspan=2, row=0)

        custom_Image(self.navbar, image=paths / "../assets/Logo.png", 
                     bg=self.master.color_background, 
                     width=571, height=82, 
                     column=0, columnspan=2, row=0)
        
        custom_Button(self.navbar, image=paths / "../assets/menu/Return.png",
                      command=self.master.home,
                      bg=self.master.color_second,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(0, 20))


        "------ Bouton du menu -------------------------------------------------------------------"
        custom_Button(self, 
                        command=self.master.menuSolo, 
                        image=paths / "../assets/menu/Solo.png",
                        height=280, width=268, 
                        bg=self.master.color_background,
                        column=0, row=1, padx=(30, 0), ipadx=5, ipady=2)
        
        custom_Button(self, 
                        command=self.master.menuDuo, 
                        image=paths / "../assets/menu/Duo.png",
                        height=280, width=268,
                        bg=self.master.color_background,
                        column=1, row=1, padx=(0, 30), ipadx=5, ipady=2)
    
        custom_Button(self, 
                        command=self.master.menuPortail, 
                        image=paths / "../assets/menu/Portail.png",
                        height=168, width=571,
                        bg=self.master.color_background,
                        column=0, row=2, ipadx=5, ipady=2, columnspan=2)