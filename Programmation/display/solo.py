from tkinter import *
from tkinter import font
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

from other.json.readJsonFile import readJsonFile

paths = Path(__file__).parent.resolve()



class displaySolo(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.grid_columnconfigure(0, weight=1)

        fileData = readJsonFile(paths / "../data/data.json").get()
        try:
            self.userName = fileData["score"][0]["name"]
        except:
            self.userName = "---------------"

        try:
            self.userScore = fileData["score"][0]["score"]
        except:
            self.userScore = 0

        self.addComponents()

    def addComponents(self):
        custom_Image(self, image=paths / "../assets/Background.png", 
                     bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, row=0, rowspan=3)


        self.navbar = Frame(self)
        self.navbar.grid(column=0, row=0)

        custom_Image(self.navbar, image=paths / "../assets/solo/Header_Solo.png", 
                     bg=self.master.color_background, 
                     width=571, height=82, 
                     column=0, columnspan=2, row=0)
        
        custom_Button(self.navbar, image=paths / "../assets/Home.png",
                      command=self.master.startGame,
                      bg=self.master.color_second,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(0, 20))
    

        self.score = Frame(self)
        self.score.grid(column=0, row=1, sticky=S)
        self.score.grid_columnconfigure(0, weight=1)
        self.score.grid_columnconfigure(1, weight=1)
        self.score.grid_columnconfigure(2, weight=15)

        custom_Image(self.score, image=paths / "../assets/Frame1.png", 
                     bg=self.master.color_background, 
                     height=84, width=571, 
                     column=0, row=0, columnspan=3)

        custom_Image(self.score, image=paths / "../assets/solo/Trophy.png",
                     bg=self.master.color_second,
                     width=50, height=50, 
                     column=0, row=0, 
                     sticky=W, padx=(20, 0))
        
        fontStyle = font.Font(size=22)
        self.name = Label(self.score, text=self.userName, font=fontStyle, 
                          bg=self.master.color_second, fg=self.master.color_text)
        self.name.grid(column=1, row=0)

        fontStyle = font.Font(size=30, weight="bold")
        self.percentage = Label(self.score, text=str(self.userScore) + "%", font=fontStyle, 
                                bg=self.master.color_second, fg=self.master.color_text)
        self.percentage.grid(column=2, row=0, sticky=E, padx=(0, 20))


        self.quiz = Frame(self)
        self.quiz.grid(column=0, row=2)
        custom_Image(self.quiz, image=paths / "../assets/Frame2.png", 
                     bg=self.master.color_background, 
                     height=320, width=571, 
                     column=0, row=0, rowspan=2, columnspan=3)
        
        self.quiz.grid_rowconfigure(0, weight=1)
        self.quiz.grid_rowconfigure(1, weight=1)
        self.quiz.grid_columnconfigure(0, weight=1)
        self.quiz.grid_columnconfigure(1, weight=1)
        self.quiz.grid_columnconfigure(2, weight=1)

        fontStyle = font.Font(size=25, weight="bold")
        self.text = Label(self.quiz, text="Choisis le nombre de questions et réalise ton meilleur score", wraplength=525, 
                          bg=self.master.color_second, fg=self.master.color_text, font=fontStyle)
        self.text.grid(column=0, columnspan=3, row=0, pady=0)

        fontStyle = font.Font(size=35, weight="bold")
        custom_Button(self.quiz, image=paths / "../assets/Button2.png", 
                      command=lambda: self.master.startQuizSolo(10),
                      text="10", font=fontStyle,
                      width=120, height=120,
                      bg=self.master.color_second, fg=self.master.color_text,
                      column=0, row=1)
        custom_Button(self.quiz, image=paths / "../assets/Button2.png",
                      command=lambda: self.master.startQuizSolo(20),
                      text="20", font=fontStyle,
                      width=120, height=120,
                      bg=self.master.color_second, fg=self.master.color_text,
                      column=1, row=1)
        custom_Button(self.quiz, image=paths / "../assets/Button2.png", 
                      command=lambda: self.master.startQuizSolo(30),
                      text="30", font=fontStyle,
                      width=120, height=120,
                      bg=self.master.color_second, fg=self.master.color_text,
                      column=2, row=1)
        