from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, ImageDraw
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

from other.chrono import ChronoApp
from other.score import scoreApp

paths = Path(__file__).parent.resolve()



class displayClick1(Frame):
    """
    interface du quiz Partie 4 - Jeux a trouver l'endroit sur la carte du monde
    """

    def __init__(self, master, callback, textQuestion, correctResponse, 
                 style=1, playerPoint=[0, 0], time=60, currentQuestion = 0, maxQuestion=20, cursorStyle=1):
        super().__init__(master)
        self.callback = callback
        
        self.style = style
        self.cursorStyle = cursorStyle
        self.time = time
        self.playerPoint = playerPoint

        self.textQuestion = textQuestion
        self.correctResponse = correctResponse

        self.questionNumber = f"{currentQuestion}/{maxQuestion}"
        self.responseDistance = [0, 0]
        self.errorRate = [50, 25, 12, 12]
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
        "------ Style de la fenetre -------------------------------------------------------------------"
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


        "------ Question -------------------------------------------------------------------"
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
        

        "------ Elements de la question -------------------------------------------------------------------"
        self.body = Frame(self, bg=self.master.color_background, height=325, width=620)
        self.body.grid(column=0, row=1)

        self.canvas = Canvas(self.body, height=310, width=620, bg=self.master.color_second, highlightthickness=4, highlightbackground="white")
        self.canvas.grid(column=0, row=0)
        self.photo = ImageTk.PhotoImage(Image.open(paths / "../../assets/quiz/World.png"))
        self.canvas.create_image(620 // 2 + 4, 310 // 2 + 4, anchor=CENTER, image=self.photo)
        self.canvas.bind("<Button-1>", self.on_click)


        "------ Valider la réponse et numero de la question -------------------------------------------------------------------"
        custom_Button(self, 
                        command=self.validate, 
                        image=paths / "../../assets/quiz/Valider.png",
                        height=75, width=343,
                        bg=self.master.color_background,
                        column=0, row=2, ipadx=5, ipady=2)
        
        fontStyle = font.Font(size=25, weight="bold")
        self.numberQuestion = Label(self, text=self.questionNumber, compound="center", font=fontStyle, fg=self.master.color_text2, bg=self.master.color_background)
        self.numberQuestion.grid(column=0, row=2, sticky=SE, padx=20, pady=20)

        
        "------ Lancer le chronometre -------------------------------------------------------------------"
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
    

    "Savoir quand et ou as cliqué l'utilisateur"
    def on_click(self, event):
        x, y = event.x, event.y
        self.responseDistance = [x, y]

        if self.cursorStyle >= 4:
            self.image = ImageTk.PhotoImage(Image.open(paths / "../../assets/quiz/Location.png"))

            self.canvas.create_image(
                x, y, anchor=S,
                image=self.image, tags="circle"
            )
        else:
            radius = [[50, 5], [25, 4], [12, 3]]
            size = (radius[self.cursorStyle - 1][0] * 2, radius[self.cursorStyle - 1][0] * 2)
            circle_image = Image.new("RGBA", size, (0, 0, 0, 0))

            draw = ImageDraw.Draw(circle_image)
            draw.ellipse((0, 0, size[0] - 2, size[1] - 2), fill=(200, 61, 61, 200), outline=(193, 30, 30, 200), width=radius[self.cursorStyle - 1][1])

            self.image = ImageTk.PhotoImage(circle_image)

            self.canvas.create_image(
                x - radius[self.cursorStyle - 1][0], y - radius[self.cursorStyle - 1][0], anchor="nw",
                image=self.image, tags="circle"
            )
    

    "Valider et corriger la réponse"
    def validate(self):
        if self.style != 2 and self.style != 3:
            self.chrono.stop_timer()

        if (self.responseDistance[0] >= self.correctResponse[0] - self.errorRate[self.cursorStyle - 1] and 
            self.responseDistance[0] <= self.correctResponse[0] + self.errorRate[self.cursorStyle - 1]) and (
            self.responseDistance[1] >= self.correctResponse[1] - self.errorRate[self.cursorStyle - 1] and 
            self.responseDistance[1] <= self.correctResponse[1] + self.errorRate[self.cursorStyle - 1]):

            self.points = 1

        if self.callback:
            self.callback()

    "Retourner le score"
    def get(self):
        return self.points