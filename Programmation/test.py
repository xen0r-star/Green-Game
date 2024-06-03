from tkinter import *
import ctypes as ct
from pathlib import Path

from display.menu import displayMenu

from display.quiz.audio1 import displayAudio
from display.quiz.choice1 import displayChoice1
from display.score import displayScore

paths = Path(__file__).parent.resolve()



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
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # self.display_start = displayAudio(self, self.e, "zzzzzzzzzzzzzzzzzzzzzzz", ["yyyyyyyy", "dddddddd", "eeeeeeeee"], 2, paths / "./data/son1.mp3")
        # self.display_start = displayChoice1(self, self.e, "zzzzzzzzzzzzzzzzzzzzzzz", ["yyyyyyyy", "dddddddd", "eeeeeeeee", "eeee"], 2)
        self.display_start = displayScore(self, 78, ["0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789", "eeeeeeeeeeeeeeeeeeeeeeee","eeeeeeeeeeeeeeeeeeeeeeee","eeeeeeeeeeeeeeeeeeeeeeee","eeeeeeeeeeeeeeeeeeeeeeee"])
        self.display_start.grid(row=0, column=0, sticky="nsew")

        self.mainloop()

    def e(self):
        pass

    def home(self):
        pass
    

    def startGame(self):
        for content in self.display_start.grid_slaves():
            content.grid_remove()

        self.display_menu = displayMenu(self)
        self.display_menu.grid(row=0, column=0, sticky="nsew")
               
        print("Start Game")


if __name__ == "__main__":
    Window().display()
