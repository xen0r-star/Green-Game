from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

from other.chrono import ChronoApp
from other.score import scoreApp

paths = Path(__file__).parent.resolve()



class displayChoice1(Frame):
    def __init__(self, master, callback, textQuestion, textResponse, correctResponse, style=1, playerPoint=[0, 0], time=60, currentQuestion = 0, maxQuestion=20):
        super().__init__(master)
        self.callback = callback
        
        self.style = style
        self.time = time
        self.playerPoint = playerPoint
        
        self.textQuestion = textQuestion
        self.textResponse = textResponse
        self.correctResponse = correctResponse

        self.questionNumber = f"{currentQuestion}/{maxQuestion}"
        self.questionNumberSelect = 0
        self.points = 0

        for content in self.master.grid_slaves():
            content.grid_remove()

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.grid_columnconfigure(0, weight=1)

        self.addComponents()


    def addComponents(self):
        if self.style == 2:
            background_source = paths / "../../assets/Background-red.png"
            self.master.color_background = "#CF6953"
        elif self.style == 3:
            background_source = paths / "../../assets/Background-blue.png"
            self.master.color_background = "#53B1CF"
        else:
            background_source = paths / "../../assets/Background.png"

        custom_Image(self, image=background_source, bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, row=0, rowspan=3)

        self.question = Frame(self, bg=self.master.color_background)
        self.question.grid(column=0, row=0)

        fontStyle = font.Font(size=15)
        custom_Image(self.question, image=paths / "../../assets/Frame5.png",
                     text=self.textQuestion, 
                     fg=self.master.color_text, font=fontStyle, wraplength=600,
                     bg=self.master.color_background, 
                     width=625, height=100, 
                     column=0, row=1)
        
        fontStyle = font.Font(size=15, weight="bold")
        
        self.header = Label(self.question, compound="center", font=fontStyle, fg=self.master.color_text, bg=self.master.color_background)
        self.header.grid(column=0, row=2, pady=(7, 0))
        

        self.body = Frame(self, bg=self.master.color_background, height=325, width=620)
        self.body.grid(column=0, row=1)

        self.button_borders = []
        for i in range(4):
            self.createButton(i, self.textResponse[i], i + 1)
            

        custom_Button(self, 
                        command=self.validate, 
                        image=paths / "../../assets/quiz/Valider.png",
                        height=75, width=343,
                        bg=self.master.color_background,
                        column=0, row=2, ipadx=5, ipady=2)
        

        fontStyle = font.Font(size=25, weight="bold")
        self.numberQuestion = Label(self, text=self.questionNumber, compound="center", font=fontStyle, fg=self.master.color_text2, bg=self.master.color_background)
        self.numberQuestion.grid(column=0, row=2, sticky=SE, padx=20, pady=20)


        if self.style == 2 or self.style == 3:
            image = scoreApp().get()

            self.header.config(image=image)
            self.header.image = image

        else:
            photo = ImageTk.PhotoImage(
                Image.open(paths / "../../assets/Frame6.png").resize((250, 40), Image.LANCZOS)
            )
            self.header.config(image=photo)
            self.header.image = photo
            self.chrono = ChronoApp(self.master, self, self.header, self.time)

    
    def createButton(self, row, text, button_number):
        buttonBorder = Frame(self.body, bg="white")
        buttonBorder.grid(column=0, row=row, pady=7)
        fontStyle = font.Font(size=15, weight="bold")
        button = Button(buttonBorder, text=text, font=fontStyle, justify='right', 
                           width=50, height=2, cursor="hand2",
                           fg=self.master.color_text, bg=self.master.color_fourth, bd=0, 
                           highlightthickness=4, highlightbackground="white", highlightcolor="white",
                           activebackground=self.master.color_fourth, activeforeground=self.master.color_text,
                           command=lambda: self.changeBorderColor(buttonBorder, button_number))
        button.grid(column=0, row=0, padx=5, pady=5)
        self.button_borders.append(buttonBorder)
    
    def changeBorderColor(self, selected_border, button_number):
        for border in self.button_borders:
            border.config(bg="white")

        selected_border.config(bg="#114232")
        self.questionNumberSelect = button_number
    

    def validate(self):
        if self.style != 2 and self.style != 3:
            self.chrono.stop_timer()

        if self.questionNumberSelect == self.correctResponse:
            self.points = 1

        if self.callback:
            self.callback()
    
    def get(self):
        return self.points
