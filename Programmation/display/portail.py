from tkinter import *
from tkinter import font
from pathlib import Path
from PIL import Image, ImageTk

from widgets.Image import custom_Image
from widgets.Button import custom_Button

from other.firebase.firestore import connexionPortail
from other.json.JsonFile import readJsonFile

paths = Path(__file__).parent.resolve()



class displayPortail(Frame):
    """
        Classe de l'écran du menu pour jouer avec le portail (Portail)
    """

    def __init__(self, master):
        super().__init__(master)

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        "------ Charger les données du meilleur score -------------------------------------------------------------------"
        fileData = readJsonFile(paths / "../data/data.json").get()
        try:
            if len(fileData["score"]) > 0:
                bestScore = 0
                for i in range(len(fileData["score"])):
                    if bestScore <=  fileData["score"][i]["score"]:
                        bestScore = fileData["score"][i]["score"]
                        try:
                            self.userName = fileData["score"][i]["name"]
                        except:
                            self.userName = "Inconnue"

                        self.userScore = fileData["score"][i]["score"]
            else:
                self.userName = "Inconnue"
                self.userScore = 0
        except:
            self.userName = "Inconnue"
            self.userScore = 0

        self.addComponents()


    def addComponents(self):
        custom_Image(self, image=paths / "../assets/Background.png", 
                     bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, columnspan=2, row=0, rowspan=4)


        "------ Barre de navigation -------------------------------------------------------------------"
        self.navbar = Frame(self)
        self.navbar.grid(column=0, columnspan=2, row=0)

        custom_Image(self.navbar, image=paths / "../assets/portail/Header_Portail.png", 
                     bg=self.master.color_background, 
                     width=571, height=82, 
                     column=0, columnspan=2, row=0)
        
        custom_Button(self.navbar, image=paths / "../assets/Home.png",
                      command=self.master.startGame,
                      bg=self.master.color_second,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(0, 20))


        "------ Partie 1 - Meilleur score -------------------------------------------------------------------"
        self.score = Frame(self)
        self.score.grid(column=0, row=1, columnspan=2, sticky=S)
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
        
        fontStyle = font.Font(size=30, weight="bold")
        self.name = Label(self.score, text=self.userName, font=fontStyle, 
                          bg=self.master.color_second, fg=self.master.color_text)
        self.name.grid(column=1, row=0)

        fontStyle = font.Font(size=30, weight="bold")
        self.percentage = Label(self.score, text=str(self.userScore) + "%", font=fontStyle, 
                                bg=self.master.color_second, fg=self.master.color_text)
        self.percentage.grid(column=2, row=0, sticky=E, padx=(0, 20))


        "------ Partie 2 - Connexion aux portails -------------------------------------------------------------------"
        self.frame = Frame(self)
        self.frame.grid(column=0, columnspan=2, row=2)

        custom_Image(self.frame, image=paths / "../assets/Frame3.png", 
                     bg=self.master.color_background, 
                     height=274, width=571, 
                     column=0, row=0, rowspan=3)

        fontStyle = font.Font(size=25, weight="bold")
        self.text = Label(self.frame, text="Saisir le code au démarrage du portail pour te connecter", wraplength=487, 
                          bg=self.master.color_second, fg=self.master.color_text, font=fontStyle)
        self.text.grid(column=0, row=0, pady=0)

        fontStyle = font.Font(size=27, weight="bold")
        self.entry = Text(self.frame, bg=self.master.color_fourth, 
                          width=20, height=1, 
                          font=fontStyle, fg=self.master.color_text, insertbackground=self.master.color_text, 
                          highlightthickness=4, highlightbackground="white", highlightcolor="white")
        self.entry.grid(column=0, row=1, ipadx=5)
        self.center_text(None)
        self.entry.bind("<KeyRelease>", self.center_text)

        photo = ImageTk.PhotoImage(
            Image.open(paths / "../assets/portail/Connexion.png").resize((303, 51), Image.LANCZOS)
        )
        self.button_connexion = Button(self.frame, command=lambda: self.connexion(self.entry.get(1.0, END).replace('\n', '')), image=photo, 
                                    bg=self.master.color_second,
                                    cursor="hand2", compound=CENTER, 
                                    bd=0, highlightthickness=0, highlightbackground="white", 
                                    activebackground=self.master.color_second)
        self.button_connexion.image = photo
        self.button_connexion.grid(column=0, row=2, ipadx=5, ipady=2)
    
    
    "Centrer le texte (widget Text)"
    def center_text(self, event):
        self.entry.tag_configure("center", justify='center')
        self.entry.tag_add("center", "1.0", "end")


    "Se connecter au portail"
    def connexion(self, token):
        self.join_group_connexion = connexionPortail(token)
        if self.join_group_connexion.report:
            self.master.startQuizPortail(token)
