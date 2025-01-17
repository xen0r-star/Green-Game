from tkinter import *
import ctypes as ct
import logzero
import os
from logzero import logger
from pathlib import Path

from display.start import displayStart
from display.menu import displayMenu

from display.solo import displaySolo
from display.duo import displayDuo
from display.portail import displayPortail

from other.game.solo import solo
from other.game.duo import duo
from other.game.portail import portail


log_directory = os.path.expanduser("~\\AppData\\Local\\GreenGenius")
Path(log_directory).mkdir(parents=True, exist_ok=True)
log_file = os.path.join(log_directory, "logFile.log")
logzero.logfile(log_file)



class Window(Tk):
    def __init__(self):
        self.color_background = "#BFEA7C"
        self.color_second = "#114232"
        self.color_third = "#9BCF53"
        self.color_fourth = "#82BA35"
        self.color_text = "#ffffff"
        self.color_text2 = "#000000"

        super().__init__()
        self.title("Green Genius")
        self.geometry(f"{700}x{700}+{(self.winfo_screenwidth() - 700) // 2}+40")
        self.resizable(False, False)
        self.config(bg=self.color_background)
        self.titleBar()


    def titleBar(self):
        """
            Changer la couleur de la barre de titre de la fenêtre Windows
        """
        
        self.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(self.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

    def display(self):
        """
            Fonction principale qui va lancer l'affichage de la première fenêtre et démarrer le programme
        """

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.home()

        try:
            self.mainloop()
        except KeyboardInterrupt:
            logger.info("App stopped.")



    def home(self):
        """
            Lance la classe de l'écran principal avec l'animation du modèle
        """

        self.display_start = displayStart(self)
        self.display_start.grid(row=0, column=0, sticky="nsew")

        logger.info("Home display")

    def startGame(self):
        """
            Lance la classe de l'écran du menu (solo, duo, portail)
        """

        for content in self.display_start.grid_slaves():
            content.grid_remove()

        self.display_menu = displayMenu(self)
        self.display_menu.grid(row=0, column=0, sticky="nsew")

        logger.info("Start Game")



    def menuSolo(self):
        """
            Lance la classe de l'écran du menu pour jouer seul (Solo)
        """

        for content in self.display_menu.grid_slaves():
            content.grid_remove()
        
        self.display_solo = displaySolo(self)
        self.display_solo.grid(row=0, column=0, sticky="nsew")

        logger.info("Solo Game")

    def menuDuo(self):
        """
            Lance la classe de l'écran du menu pour jouer à deux (Duo)
        """

        for content in self.display_menu.grid_slaves():
            content.grid_remove()

        self.question, self.listQuestion = [], []
        self.display_duo = displayDuo(self)
        self.display_duo.grid(row=0, column=0, sticky="nsew")
            
        logger.info("Duo Game")

    def menuPortail(self):
        """
            Lance la classe de l'écran du menu pour jouer avec le portail (Portail)
        """

        for content in self.display_menu.grid_slaves():
            content.grid_remove()
        
        self.display_portail = displayPortail(self)
        self.display_portail.grid(row=0, column=0, sticky="nsew")
        
        logger.info("Portail Game")



    def startQuizSolo(self, numberQuestion=20):
        """
            Lance la classe qui va démarrer le jeu en solo (Solo)
        """

        for content in self.grid_slaves():
            content.grid_remove()

        solo(self, numberQuestion)

        logger.info("Start Solo Game")
    

    def startQuizDuo(self, user, token):
        """
            Lance la classe qui va démarrer le jeu à deux (Duo)
        """

        for content in self.grid_slaves():
            content.grid_remove()

        duo(self, 20, user, token)

        logger.info("Start Duo Game")


    def startQuizPortail(self, token):
        """
            Lance la classe qui va démarrer le jeu avec le portail (Portail)
        """

        for content in self.grid_slaves():
            content.grid_remove()

        portail(self, 10, token)

        logger.info("Start Portail Game")



if __name__ == "__main__":
    Window().display()