from tkinter import *
from tkinter import font
from pathlib import Path
from PIL import Image, ImageTk

from widgets.Image import custom_Image
from widgets.Button import custom_Button

paths = Path(__file__).parent.resolve()



class displayScore(Frame):
    def __init__(self, master, playerScore, errorQuestion):
        super().__init__(master)
        self.playerScore = playerScore
        self.errorQuestion = errorQuestion[:4]

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=8)
        self.grid_columnconfigure(0, weight=1)

        self.addComponents()

    def addComponents(self):
        custom_Image(self, image=paths / "../assets/Background.png", 
                     bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, row=0, rowspan=3)


        self.navbar = Frame(self)
        self.navbar.grid(column=0, row=0)

        custom_Image(self.navbar, image=paths / "../assets/score/Header_Score.png", 
                     bg=self.master.color_background, 
                     width=571, height=82, 
                     column=0, columnspan=2, row=0)
        
        custom_Button(self.navbar, image=paths / "../assets/Home.png",
                      command=self.master.startGame,
                      bg=self.master.color_second,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(0, 20))

        fontStyle = font.Font(size=55, weight="bold")
        custom_Image(self, image=paths / "../assets/score/Frame1.png",
                     text=str(self.playerScore) + " %", font=fontStyle, fg=self.master.color_text,
                     bg=self.master.color_background, 
                     width=240, height=126, 
                     column=0, row=1)

        self.frame = Frame(self, bg=self.master.color_background, width=571, height=370)
        self.frame.grid(column=0, row=2, sticky=NSEW, padx=64)

        self.frame.grid_columnconfigure(0, weight=1)
        fontStyle = font.Font(size=15, weight="bold")

        for i in range(len(self.errorQuestion)):
            elementErrorQuestion = Frame(self.frame, bg=self.master.color_second, width=571, height=64, 
                                         highlightthickness=4, highlightbackground="white", highlightcolor="white",)
            elementErrorQuestion.grid(row=i, column=0, pady=(0, 10), sticky="ew")
            self.frame.grid_rowconfigure(i, weight=1)

            elementErrorQuestion.grid_columnconfigure(0, weight=1)
            elementErrorQuestion.grid_columnconfigure(1, weight=1)

            custom_Image(elementErrorQuestion, paths / "../assets/score/Error.png", width=50, height=50, bg=self.master.color_second, 
                         row=0, column=0, sticky=W, padx=(10, 5))
            
            if len(self.errorQuestion[i]) > 40:
                label = Label(elementErrorQuestion, text=self.errorQuestion[i][:38] + "...", 
                                font=fontStyle, fg=self.master.color_text, bg=self.master.color_second, justify=RIGHT)
            else:
                label = Label(elementErrorQuestion, text=self.errorQuestion[i].ljust(38 - len(self.errorQuestion[i])), width=38, 
                                font=fontStyle, fg=self.master.color_text, bg=self.master.color_second, justify=RIGHT)
            
            label.grid(row=0, column=1, padx=0, pady=20, sticky="w")