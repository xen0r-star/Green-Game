from tkinter import *
from PIL import Image, ImageTk
import ctypes as ct
from pathlib import Path

from widgets.Button import custom_Button

paths = Path(__file__).parent.resolve()

class Window(Tk):
    def __init__(self):
        self.color_background = "#4CCD99"
        self.color_second = "#007F73"
        self.color_text = "#ffffff"

        super().__init__()
        self.title("Name Jeux")
        self.geometry(f"{700}x{700}+{(self.winfo_screenwidth() - 700) // 2}+40")
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

        self.display_start = displayStart(self)
        self.display_start.grid(row=0, column=0, sticky="nsew")

        self.mainloop()



    def startGame(self):
        for content in self.display_start.grid_slaves():
            content.grid_remove()

        self.display_Menu = displayMenu(self)
        self.display_Menu.grid(row=0, column=0, sticky="nsew")
               
        print("Start Game")



    def startSolo(self):
        for content in self.display_Menu.grid_slaves():
            content.grid_remove()
               
        print("Solo Game")

    def startDuo(self):
        for content in self.display_Menu.grid_slaves():
            content.grid_remove()
               
        print("Duo Game")

    def startPortail(self):
        for content in self.display_Menu.grid_slaves():
            content.grid_remove()
               
        print("Portail Game")


class displayStart(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")
        self.addComponents()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def addComponents(self):
        square = Canvas(self, height=391, width=540, bg=self.master.color_second)
        square.grid(column=0, row=0, padx=10, pady=10)
        
        button = custom_Button(self, 
                               command=self.master.startGame, 
                               text="J O U E R",
                               image=paths / "assets/Button.png",
                               height=70, width=325,
                               bg=self.master.color_background, fg=self.master.color_text, 
                               column=0, row=1, padx=10, pady=10, ipadx=5, ipady=2)
    

class displayMenu(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")
        self.addComponents()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def addComponents(self):
        photo = ImageTk.PhotoImage(
            Image.open(paths / "assets/Logo.png").resize((100, 100), Image.LANCZOS)
        )
        logo = Label(self, image=photo, bg=self.master.color_background)
        logo.image = photo
        logo.grid(column=0, columnspan=2, row=0)
        
        border_solo = Label(self, bg="white")
        border_solo.grid(column=0, row=1, padx=25, pady=25, sticky="nsew")
        button_Solo = Button(border_solo, 
                        command=self.master.startSolo, 
                        text="SOLO",
                        bg=self.master.color_second, fg=self.master.color_text,
                        cursor="hand2", 
                        bd=0, highlightthickness=0, highlightbackground="white", 
                        activebackground=self.master.color_second, activeforeground=self.master.color_text)
        button_Solo.grid(padx=5, pady=5, sticky="nsew")
        border_solo.grid_rowconfigure(0, weight=1)
        border_solo.grid_columnconfigure(0, weight=1)

        border_duo = Label(self, bg="white")
        border_duo.grid(column=1, row=1, padx=25, pady=25, sticky="nsew")
        button_Duo = Button(border_duo, 
                        command=self.master.startDuo, 
                        text="DUO",
                        bg=self.master.color_second, fg=self.master.color_text,
                        cursor="hand2", compound=CENTER, 
                        bd=0, highlightthickness=0, highlightbackground="white", 
                        activebackground=self.master.color_second, activeforeground=self.master.color_text)
        button_Duo.grid(padx=5, pady=5, sticky="nsew")
        border_duo.grid_rowconfigure(0, weight=1)
        border_duo.grid_columnconfigure(0, weight=1)
    

        border_portail = Label(self, bg="white")
        border_portail.grid(column=0, columnspan=2, row=2, padx=25, pady=25, sticky="nsew")
        button_Portail = Button(border_portail, 
                        command=self.master.startPortail, 
                        text="PORTAIL",
                        bg=self.master.color_second, fg=self.master.color_text,
                        cursor="hand2", compound=CENTER, 
                        bd=0, highlightthickness=0, highlightbackground="white", 
                        activebackground=self.master.color_second, activeforeground=self.master.color_text)
        button_Portail.grid(padx=5, pady=5, sticky="nsew")
        border_portail.grid_rowconfigure(0, weight=1)
        border_portail.grid_columnconfigure(0, weight=1)

Window().display()