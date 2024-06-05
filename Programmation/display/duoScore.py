from tkinter import *
from tkinter import font
from pathlib import Path

from widgets.Image import custom_Image
from widgets.Button import custom_Button
from other.json.JsonFile import addDataJsonFile
from other.firebase.firestore import waitEnd

paths = Path(__file__).parent.resolve()



class displayScoreDuo(Frame):
    """
    class de l'ecrant pour afficher le scrore final du joueur
    """

    def __init__(self, master, playerScore, errorQuestion = [], style=1, user=0, token=""):
        super().__init__(master)
        self.playerScore = playerScore
        self.errorQuestion = errorQuestion[:3]
        self.style = style
        self.user, self.token = user, token

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=8)
        self.grid_columnconfigure(0, weight=1)

        self.addComponents()


    def addComponents(self):
        "------ Style de la fenetre -------------------------------------------------------------------"
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
                     column=0, row=0, rowspan=3)


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


        "------ Affichage Score -------------------------------------------------------------------"
        self.frame = Frame(self)
        self.frame.grid(column=0, row=1)

        fontStyle = font.Font(size=20, weight="bold")
        custom_Image(self.frame, image=paths / "../assets/score/Frame1.png",
                     text="En attende de l'autre joueur", font=fontStyle, fg=self.master.color_text,
                     bg=self.master.color_background, 
                     width=240, height=126, 
                     column=0, row=0)

        self.waitEnd = waitEnd(token=self.token)
        if not self.waitEnd.report:
            self.check_report()
        else:
            for content in self.frame.grid_slaves():
                content.grid_remove()


    def check_report(self):
        if self.waitEnd.report:
            for content in self.frame.grid_slaves():
                content.grid_remove()
        elif self.loopCreate:
            self.master.after(1000, self.check_report)




    "Centrer le texte dans le widget Text"
    def center_text(self, event): 
        self.entry.tag_configure("center", justify='center')
        self.entry.tag_add("center", "1.0", "end")


    def saveData(self):
        addDataJsonFile({
            "name": self.entry.get(1.0, END).replace('\n', ''),
            "score": self.playerScore
        })