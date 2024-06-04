from tkinter import *
from tkinter import font, messagebox
import pygame
from logzero import logger
from PIL import Image, ImageTk, ImageDraw
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

from other.chrono import ChronoApp
from other.score import scoreApp

paths = Path(__file__).parent.resolve()



class displayAudio(Frame):
    """
    interface du quiz Partie 1 - Jeux a retourver le sens du son
    """
    def __init__(self, master, callback, textQuestion, textResponse, correctResponse, audioFile, 
                 style=1, playerPoint=[0, 0], time=60, currentQuestion = 0, maxQuestion=20):
        super().__init__(master)
        self.callback = callback
        
        self.style = style
        self.time = time
        self.playerPoint = playerPoint
        
        self.textQuestion = textQuestion
        self.textResponse = textResponse
        self.correctResponse = correctResponse
        self.audioFile = paths / "../../data/" / audioFile

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
                     column=0, row=0)
        
        fontStyle = font.Font(size=15, weight="bold")
        
        self.header = Label(self.question, compound="center", font=fontStyle, fg=self.master.color_text, bg=self.master.color_background)
        self.header.grid(column=0, row=1, pady=(7, 0))
        

        "------ Elements de la question -------------------------------------------------------------------"
        self.body = Frame(self, bg=self.master.color_background, height=325, width=620)
        self.body.grid(column=0, row=1)

        self.audio = Frame(self.body, bg=self.master.color_second, 
                           width=622, height=55, 
                           highlightthickness=4, highlightbackground="white", highlightcolor="white")
        self.audio.grid(column=0, row=0, pady=(10, 20))
        self.audio.grid_columnconfigure(0, weight=1)
        self.audio.grid_columnconfigure(1, weight=1)
        self.audio.grid_columnconfigure(2, weight=1)
        self.audio.grid_columnconfigure(3, weight=1)

        fontStyle = font.Font(size=15, weight="bold")
        self.audioTime = Label(self.audio, text="00:00", font=fontStyle, fg=self.master.color_text, bg=self.master.color_second)
        self.audioTime.grid(column=0, row=0, padx=(10, 0))
        
        image = self.timeBar(0, 10)
        photo = ImageTk.PhotoImage(image)
        self.audioTimeBar = Label(self.audio, image=photo, bg=self.master.color_second)
        self.audioTimeBar.image = photo
        self.audioTimeBar.grid(column=1, row=0, padx=10, pady=15)

        self.buttonPlayStat = "Start"
        photo = ImageTk.PhotoImage(
            Image.open(paths / "../../assets/quiz/Pause.png").resize((35, 35), Image.LANCZOS)
        )
        self.buttonPlay = Button(self.audio, command=self.play_pause, image=photo,
                        bg=self.master.color_second, 
                        cursor="hand2", bd=0, highlightthickness=0, highlightbackground="white", 
                        activebackground=self.master.color_second)
        self.buttonPlay.image = photo
        self.buttonPlay.grid(row=0, column=2, padx=10)

        self.button_borders = []
        for i in range(3):
            self.createButton(i + 1, self.textResponse[i], i + 1)
            

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
        photo = ImageTk.PhotoImage(
            Image.open(paths / "../../assets/Frame6.png").resize((250, 40), Image.LANCZOS)
        )
        self.header.config(image=photo)
        self.header.image = photo
        self.chrono = ChronoApp(self.master, self, self.header, self.time)


    "Mettre Play et Pause au son"
    def play_pause(self):
        if self.buttonPlayStat == "Start":
            self.buttonPlayStat = "Play"
            self.start_sound()

            photo = ImageTk.PhotoImage(
                Image.open(paths / "../../assets/quiz/Play.png").resize((35, 35), Image.LANCZOS)
            )
            self.buttonPlay.config(image=photo)
            self.buttonPlay.image = photo

            self.update_progress()

        elif self.buttonPlayStat == "Play":
            self.buttonPlayStat = "Pause"
            pygame.mixer.music.pause()

            photo = ImageTk.PhotoImage(
                Image.open(paths / "../../assets/quiz/Pause.png").resize((35, 35), Image.LANCZOS)
            )
            self.buttonPlay.config(image=photo)
            self.buttonPlay.image = photo
        else:
            self.buttonPlayStat = "Play"
            pygame.mixer.music.unpause()
            self.update_progress()

            photo = ImageTk.PhotoImage(
                Image.open(paths / "../../assets/quiz/Play.png").resize((35, 35), Image.LANCZOS)
            )
            self.buttonPlay.config(image=photo)
            self.buttonPlay.image = photo
    

    "Charger et démarer le son"
    def start_sound(self):
        try:
            pygame.mixer.init()
            self.totalTimeSound = pygame.mixer.Sound(self.audioFile).get_length()
            pygame.mixer.music.load(self.audioFile)
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as _:
            self.error()
    

    "Mettre a jour la barre de progression"
    def update_progress(self):
        try:
            self.current_time = int(pygame.mixer.music.get_pos() // 1000 % self.totalTimeSound)
            minutes = self.current_time // 60
            seconds = self.current_time % 60
            self.audioTime.config(text=f"{minutes:02}:{seconds:02}")
            if pygame.mixer.music.get_busy():
                self.master.after(1000, self.update_progress)

            image = self.timeBar(self.current_time, self.totalTimeSound)
            photo = ImageTk.PhotoImage(image)
            self.audioTimeBar.config(image=photo)
            self.audioTimeBar.image = photo
        except pygame.error as e:
            self.error()


    "Faire l'image de la barre de progression"
    def timeBar(self, current, total):
        image = Image.new("RGBA", (420, 10), "#ffffff00")
        draw = ImageDraw.Draw(image)

        time = (current / total) * 100
        if time < 10:
            time = 10
        rect2_coords = (0, 0, (time / 100) * 420, 10)

        def draw_rounded_rectangle(draw, coords, radius, fill):
            x1, y1, x2, y2 = coords
            draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
            draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
            draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
            draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
            draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
            draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)

        draw_rounded_rectangle(draw, (0, 0, 420, 10), 5, fill="#747977")
        draw_rounded_rectangle(draw, rect2_coords, 5, fill="#FF3D3D")

        return image


    "Crée le bouton"
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
    
    "Changer la couleur du bouton a son clique"
    def changeBorderColor(self, selected_border, button_number):
        for border in self.button_borders:
            border.config(bg="white")

        selected_border.config(bg="#114232")
        self.questionNumberSelect = button_number
    

    "Valider et corriger la réponse"
    def validate(self):
        if self.style != 2 and self.style != 3:
            self.chrono.stop_timer()

        if self.questionNumberSelect == self.correctResponse:
            self.points = 1

        if self.callback:
            self.callback()
    
    "Retourner le score"
    def get(self):
        return self.points


    def error(self):
        logger.error("Erreur 50")
        self.master.home()
        messagebox.showwarning("Erreur 50", "Une erreur s'est produite lors de la lecture du fichier audio")

