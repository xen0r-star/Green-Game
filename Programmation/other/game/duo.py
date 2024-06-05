from tkinter import messagebox
from pathlib import Path
from logzero import logger

from other.firebase.firestore import userPoints, endGame

from display.quiz.choice1 import displayChoice1
from display.quiz.choice2 import displayChoice2
from display.quiz.click1 import displayClick1
from display.quiz.DragAndDrop1 import displayDragAndDrop1
from display.quiz.DragAndDrop2 import displayDragAndDrop2
from display.quiz.DragAndDrop3 import displayDragAndDrop3
from display.quiz.audio1 import displayAudio
from display.duoScore import displayScoreDuo

paths = Path(__file__).parent.resolve()



class duo:
    """
    class qui permets de gérer le cours de la partie a deux (Duo)
    """
    
    def __init__(self, master, numberQuestion, user, token):
        self.numberQuestion = numberQuestion
        self.master = master
        self.user = user
        self.token = token

        self.readFile = self.master.question
        self.playerScore = 0

        if self.readFile == []:
            self.error()
        
        self.userPoints = userPoints(self.user, self.token)

        self.start()
        self.play()


    def start(self):
        logger.info("Play Duo Game")

        self.listeType = []
        for data in self.readFile:
            self.listeType.append(data["type"])

        self.randomList = self.master.listQuestion
        self.currentQuestionIndex = 0
        

    def play(self):
        function = {
            "choice1": self.Choice1,
            "choice2": self.Choice2,
            "click1": self.Click1,
            "draganddrop1": self.DragAndDrop1,
            "draganddrop2": self.DragAndDrop2,
            "draganddrop3": self.DragAndDrop3,
            "audio1": self.Audio1
        }

        if self.currentQuestionIndex > 0:
            self.userPoints.set(self.display.get())
            self.playerScore += self.display.get()

        if self.currentQuestionIndex < len(self.randomList):
            question_type = self.listeType[self.randomList[self.currentQuestionIndex]]
            if question_type in function:
                question_class = function[question_type]
                question_class()
            else:
                self.error()
                
            self.currentQuestionIndex += 1
        else:
            endGame(self.token, self.user)
            logger.info(f"End quiz, score player: {self.playerScore} ({int((self.playerScore / len(self.randomList)) * 100)})")
            displayScoreDuo(self.master, int((self.playerScore / len(self.randomList)) * 100), style=self.user + 1, user=self.user, token=self.token)



    "------ Fonction des different interface du quiz -------------------------------------------------------------------"
    
    def Choice1(self):
        self.display = displayChoice1(self.master, self.play, 
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.randomList),
                                            playerPoint=self.userPoints.get(),
                                            style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def Choice2(self):
        self.display = displayChoice2(self.master, self.play, 
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.randomList),
                                            playerPoint=self.userPoints.get(),
                                            style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def Click1(self):
        self.display = displayClick1(self.master, self.play, 
                                           self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                           self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                           cursorStyle=self.readFile[self.randomList[self.currentQuestionIndex]]["cursor"],
                                           time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                           currentQuestion=self.currentQuestionIndex + 1,
                                           maxQuestion=len(self.randomList),
                                           playerPoint=self.userPoints.get(),
                                           style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def DragAndDrop1(self):
        self.display = displayDragAndDrop1(self.master, self.play, 
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["answer"],
                                                 time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                                 currentQuestion=self.currentQuestionIndex + 1,
                                                 maxQuestion=len(self.randomList),
                                                 playerPoint=self.userPoints.get(),
                                                 style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def DragAndDrop2(self):
        self.display = displayDragAndDrop2(self.master, self.play, 
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["zones"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["answer"],
                                                 time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                                 currentQuestion=self.currentQuestionIndex + 1,
                                                 maxQuestion=len(self.randomList),
                                                 playerPoint=self.userPoints.get(),
                                                 style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def DragAndDrop3(self):
        self.display = displayDragAndDrop3(self.master, self.play, 
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["zones"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["answer"],
                                                 time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                                 currentQuestion=self.currentQuestionIndex + 1,
                                                 maxQuestion=len(self.randomList),
                                                 playerPoint=self.userPoints.get(),
                                                 style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")
    
    def Audio1(self):
        self.display = displayAudio(self.master, self.play, 
                                    self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                    self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                    self.readFile[self.randomList[self.currentQuestionIndex]]["answer"],
                                    self.readFile[self.randomList[self.currentQuestionIndex]]["sound"],
                                    time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                    currentQuestion=self.currentQuestionIndex + 1,
                                    maxQuestion=len(self.randomList),
                                    style=1)
        self.display.grid(row=0, column=0, sticky="nsew")


    def error(self):
        logger.error("Erreur 20")
        self.master.home()
        messagebox.showwarning("Erreur 20", 
                               "Une erreur s'est produite lors de la lecture du fichier de données des questions. Le fichier est peut être mal écrit, contient des erreurs ou est vide.")
