from tkinter import *
from tkinter import font, messagebox
from pathlib import Path
import random
from PIL import Image, ImageTk

from widgets.Image import custom_Image
from widgets.Button import custom_Button

from other.firebase.firestore import createGroup, joinGroup, storageQuestion, loadQuestion
from other.json.JsonFile import readJsonFileSchema

paths = Path(__file__).parent.resolve()



class displayDuo(Frame):
    """
        Classe de l'écran du menu pour jouer à deux (Duo)
    """

    def __init__(self, master):
        super().__init__(master)

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.addComponents()


    def addComponents(self):
        custom_Image(self, image=paths / "../assets/Background.png", 
                     bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, columnspan=2, row=0, rowspan=3)


        "------ Barre de navigation -------------------------------------------------------------------"
        self.navbar = Frame(self)
        self.navbar.grid(column=0, columnspan=2, row=0)

        custom_Image(self.navbar, image=paths / "../assets/duo/Header_Duo.png", 
                     bg=self.master.color_background, 
                     width=571, height=82, 
                     column=0, columnspan=2, row=0)
        
        custom_Button(self.navbar, image=paths / "../assets/Home.png",
                      command=self.master.startGame,
                      bg=self.master.color_second,
                      width=55, height=55,
                      column=1, row=0, sticky=E,
                      padx=(0, 20))


        "------ Partie 1 - Rejoindre/Créer un groupe -------------------------------------------------------------------"
        photo = ImageTk.PhotoImage(
            Image.open(paths / "../assets/duo/Join_Group2.png").resize((275, 204), Image.LANCZOS)
        )
        self.button_join = Button(self, command=self.join_group, image=photo, 
                                  bg=self.master.color_background, 
                                  cursor="hand2", compound=CENTER, 
                                  bd=0, highlightthickness=0, highlightbackground="white", 
                                  activebackground=self.master.color_background)
        self.button_join.image = photo
        self.button_join.grid(column=0, row=1, padx=(55, 0), ipadx=5, ipady=2)

        photo = ImageTk.PhotoImage(
            Image.open(paths / "../assets/duo/Create_Group1.png").resize((275, 204), Image.LANCZOS)
        )
        self.button_create = Button(self, command=self.create_group, image=photo, 
                                    bg=self.master.color_background, 
                                    cursor="hand2", compound=CENTER, 
                                    bd=0, highlightthickness=0, highlightbackground="white", 
                                    activebackground=self.master.color_background)
        self.button_create.image = photo
        self.button_create.grid(column=1, row=1, padx=(0, 55), ipadx=5, ipady=2)


        self.frame = Frame(self)
        self.frame.grid(column=0, columnspan=2, row=2)

        self.join_group()
    


    "Partie 2 - Interface pour rejoindre un groupe"
    def join_group(self):
        self.loopCreate = True

        "------ Changer l'image du bouton -------------------------------------------------------------------"
        photo_join = ImageTk.PhotoImage(
            Image.open(paths / "../assets/duo/Join_Group2.png").resize((275, 204), Image.LANCZOS)
        )
        self.button_join.config(image=photo_join)
        self.button_join.image = photo_join

        photo_create = ImageTk.PhotoImage(
            Image.open(paths / "../assets/duo/Create_Group1.png").resize((275, 204), Image.LANCZOS)
        )
        self.button_create.config(image=photo_create)
        self.button_create.image = photo_create

        for content in self.frame.grid_slaves():
            content.grid_remove()

        
        "------ Contenu de connexion au groupe -------------------------------------------------------------------"
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        custom_Image(self.frame, image=paths / "../assets/Frame3.png", 
                     bg=self.master.color_background, 
                     height=274, width=571, 
                     column=0, row=0, rowspan=3)

        fontStyle = font.Font(size=25, weight="bold")
        self.text = Label(self.frame, text="Saisis le code de la salle pour la rejoindre", wraplength=487, 
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
            Image.open(paths / "../assets/duo/Join_Button.png").resize((303, 51), Image.LANCZOS)
        )
        self.button_joined = Button(self.frame, command=lambda: self.join(self.entry.get(1.0, END).replace('\n', '')), image=photo, 
                                    bg=self.master.color_second,
                                    cursor="hand2", compound=CENTER, 
                                    bd=0, highlightthickness=0, highlightbackground="white", 
                                    activebackground=self.master.color_second)
        self.button_joined.image = photo
        self.button_joined.grid(column=0, row=2, ipadx=5, ipady=2)
    

    "Partie 3 - Rejoindre un groupe dans la base de données"
    def join(self, token):
        self.join_group_connexion = joinGroup(token)
        if self.join_group_connexion.report:
            self.loadQuestion = loadQuestion(token)
            self.master.question = self.loadQuestion.question
            self.master.listQuestion = self.loadQuestion.listQuestion

            self.master.startQuizDuo(1, self.entry.get(1.0, END).replace('\n', ''))



    "Partie 2.2 - Interface pour créer un groupe"
    def create_group(self):
        self.loopCreate = False

        "------ Changer l'image du bouton -------------------------------------------------------------------"
        photo_join = ImageTk.PhotoImage(
            Image.open(paths / "../assets/duo/Join_Group1.png").resize((275, 204), Image.LANCZOS)
        )
        self.button_join.config(image=photo_join)
        self.button_create.image = photo_join

        photo_create = ImageTk.PhotoImage(
            Image.open(paths / "../assets/duo/Create_Group2.png").resize((275, 204), Image.LANCZOS)
        )
        self.button_create.config(image=photo_create)
        self.button_join.image = photo_create

        for content in self.frame.grid_slaves():
            content.grid_remove()


        "------ Contenu de création du groupe -------------------------------------------------------------------"
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        custom_Image(self.frame, image=paths / "../assets/Frame3.png", 
                     bg=self.master.color_background, 
                     height=274, width=571, 
                     column=0, row=0, rowspan=2)

        fontStyle = font.Font(size=25, weight="bold")
        self.text = Label(self.frame, text="Donne le code a ton amis pour jouer a deux", wraplength=487, 
                          bg=self.master.color_second, fg=self.master.color_text, font=fontStyle)
        self.text.grid(column=0, row=0, pady=0)

        
        self.create_group_connexion = createGroup()
        self.readFile = readJsonFileSchema(paths / "../data/question.json").get()
        if self.readFile == []:
            self.error()

        self.listeType = []
        for data in self.readFile:
            self.listeType.append(data["type"])
        
        self.randomList = random.sample(range(0, len(self.listeType)), min(20, len(self.listeType)))

        storageQuestion(self.create_group_connexion.id, self.readFile, self.randomList)


        fontStyle = font.Font(size=27, weight="bold")
        self.code = custom_Image(self.frame, image=paths / "../assets/Frame4.png", 
                                 font=fontStyle, text=self.create_group_connexion.id,
                                 width=499, height=56,
                                 bg=self.master.color_second, fg=self.master.color_text, 
                                 row=1, column=0)
        
        self.check_report()
    

    "Partie 3.3 - crée un groupe dans la base de données"
    def check_report(self):
        if self.create_group_connexion.report:
            self.master.question = self.readFile
            self.master.listQuestion = self.randomList
            self.master.startQuizDuo(2, self.create_group_connexion.id)
        elif not self.loopCreate:
            self.master.after(1000, self.check_report)



    "Centrer le texte (widget Text)"
    def center_text(self, event):
        self.entry.tag_configure("center", justify='center')
        self.entry.tag_add("center", "1.0", "end")
    

    def error(self):
        self.master.home()
        messagebox.showwarning("Erreur 40", "Une erreur s'est produite lors de la lecture du fichier de données des questions. Le fichier est peut être mal écrit, contient des erreurs ou est vide.")
