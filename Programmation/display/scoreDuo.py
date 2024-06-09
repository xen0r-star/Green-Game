from tkinter import *
from tkinter import font
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk

from widgets.Image import custom_Image
from widgets.Button import custom_Button
from other.firebase.firestore import waitEnd, userPoints

paths = Path(__file__).parent.resolve()



class displayScoreDuo(Frame):
    """
        Classe de l'écran pour afficher le score final du joueur
    """

    def __init__(self, master, numberQuestion, style=2, user=0, token=""):
        super().__init__(master)
        self.numberQuestion = numberQuestion
        self.style = style
        self.user, self.token = user, token

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.addComponents()


    def addComponents(self):
        "------ Style de la fenêtre -------------------------------------------------------------------"
        if self.style == 2:
            background_source = paths / "../assets/Background-red.png"
            self.master.color_background = "#CF6953"
        elif self.style == 3:
            background_source = paths / "../assets/Background-blue.png"
            self.master.color_background = "#53B1CF"
        else:
            background_source = paths / "../../assets/Background.png"

        custom_Image(self, image=background_source, 
                     bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, row=0, rowspan=4)


        "------ Barre de navigation -------------------------------------------------------------------"
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
        
        
        self.loopCreate = True


        "------ Affichage du score -------------------------------------------------------------------"
        self.header = Frame(self)
        self.header.grid(column=0, row=1)

        fontStyle = font.Font(size=30, weight="bold")
        custom_Image(self.header, image=paths / "../assets/score/Frame2.png",
                     bg=self.master.color_background, 
                     width=453, height=126, 
                     column=0, row=0, rowspan=2)
        self.text1 = Label(self.header, text="En attente de l'autre", fg=self.master.color_text, font=fontStyle, bg=self.master.color_second)
        self.text1.grid(column=0, row=0, pady=(13, 0))
        self.text2 = Label(self.header, text="joueur", fg=self.master.color_text, font=fontStyle, bg=self.master.color_second)
        self.text2.grid(column=0, row=1, pady=(0, 13))

        "------ Création de l'emplacement pour les résultats et vérification que les deux joueurs ont fini -------------------------------------------------------------------"
        self.body = Frame(self, height=265, width=571, bg=self.master.color_background)
        self.body.grid(column=0, row=2)

        self.waitEnd = waitEnd(token=self.token)
        if not self.waitEnd.report:
            self.check_report()
        else:
            self.showScore()

    "Attend une notification de la base donnée pour dire quand les deux joueur on finie"
    def check_report(self):
        if self.waitEnd.report:
            self.waitEnd.stop_listening()
            self.showScore()
        elif self.loopCreate:
            self.master.after(1000, self.check_report)
    

    "------ Affichage des résultats -------------------------------------------------------------------"
    def showScore(self):
        score = userPoints(self.user, self.token).get()
        red = (score[0] / self.numberQuestion) * 100
        blue = (score[1] / self.numberQuestion) * 100

        if red > blue:
            self.text1.config(text="LE GAGNANT EST")
            self.text2.config(text="ROUGE", fg="#E33F3F")
        elif red < blue:
            self.text1.config(text="LE GAGNANT EST")
            self.text2.config(text="BLEU", fg="#4C98F1")
        else:
            self.text1.config(text="ÉGALITÉ")
            self.text2.config(text="AUCUN GAGNANT")
        
        fontStyle = font.Font(size=30, weight="bold")
        text = Label(self.body, text=str(red) + "%", fg=self.master.color_text, font=fontStyle, justify="left", bg=self.master.color_background)
        text.grid(column=0, row=0, sticky=W, padx=15)

        self.photoRed = ImageTk.PhotoImage(self.imageScore(red, (148, 3, 3)))
        imageRed = Label(self.body, image=self.photoRed, height=82, width=572, bg=self.master.color_background)
        imageRed.grid(column=0, row=1)


        fontStyle = font.Font(size=30, weight="bold")
        text = Label(self.body, text=str(blue) + "%", fg=self.master.color_text, font=fontStyle, justify="left", bg=self.master.color_background)
        text.grid(column=0, row=2, sticky=W, padx=15, pady=(25, 0))

        self.photoBlue = ImageTk.PhotoImage(self.imageScore(blue, (3, 70, 148)))
        imageBlue = Label(self.body, image=self.photoBlue, height=82, width=572, bg=self.master.color_background)
        imageBlue.grid(column=0, row=3)
        

    "------ Création de l'image pour les scores des joueurs -------------------------------------------------------------------"
    def imageScore(self, percentage, color):
        grey = (83, 83, 83)

        if percentage >= 100:
            grey = color
        elif percentage <= 0:
            color = (83, 83, 83)

        if percentage > 95:
            percentage = 95
        elif percentage < 5:
            percentage = 5
            

        image = Image.new('RGBA', (571, 82), (0, 0, 0, 0))

        "------ Partie 1 - Image rouge -------------------------------------------------------------------"
        redImage = Image.new('RGB', (int(571 * (percentage / 100)), 82), color)
        redMask = Image.new('L', (int(571 * (percentage / 100)), 82), 0)
        draw = ImageDraw.Draw(redMask)
        draw.rectangle((0, 20, int(571 * (percentage / 100)), 62), fill=255)
        draw.ellipse((4, 2, 34, 32), fill=255)
        draw.ellipse((4, 50, 34, 80), fill=255)
        draw.rectangle((26, 5, int(571 * (percentage / 100) - 1), 78), fill=255)

        redImage.putalpha(redMask)


        "------ Partie 2 - Image gris -------------------------------------------------------------------"
        greyImage = Image.new('RGB', (571, 82), grey)
        greyMask = Image.new('L', (571, 82), 0)
        draw = ImageDraw.Draw(greyMask)
        draw.rectangle((0, 20, 571, 62), fill=255)
        draw.ellipse((537, 2, 537 + 30, 32), fill=255)
        draw.ellipse((537, 50, 537 + 30, 80), fill=255)
        draw.rectangle((20, 5, 571 - 26, 78), fill=255)

        greyImage.putalpha(greyMask)


        "------ Partie 3 - Fusionne Image -------------------------------------------------------------------"
        image.paste(greyImage, (0, 0), greyImage)
        image.paste(redImage, (0, 0), redImage)

        borderImage = Image.open(paths / "../assets/score/border.png")

        position = ((571 - borderImage.width) // 2, (82 - borderImage.height) // 2)
        image.paste(borderImage, position, borderImage)

        if percentage < 100 and not percentage > 0:
            draw = ImageDraw.Draw(image)
            draw.rectangle((int(571 * (percentage / 100)) - 3, 5, int(571 * (percentage / 100)) + 3, 82), fill=(255, 255, 255))

        return image