from tkinter import messagebox
from pathlib import Path

from other.firebase.firestore import userPoints

from display.quiz.choice1 import displayChoice1
from display.quiz.choice2 import displayChoice2
from display.quiz.click1 import displayClick1
from display.quiz.DragAndDrop1 import displayDragAndDrop1
from display.quiz.DragAndDrop2 import displayDragAndDrop2
from display.quiz.DragAndDrop3 import displayDragAndDrop3


paths = Path(__file__).parent.resolve()


class duo:
    def __init__(self, master, numberQuestion, user, token):
        self.numberQuestion = numberQuestion
        self.master = master
        self.user = user
        self.token = token

        self.readFile = self.master.question

        if self.readFile == []:
            self.error()
        
        self.userPoints = userPoints(self.user, self.token)

        self.start()
        self.play()

    def start(self):
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
            "draganddrop3": self.DragAndDrop3
        }

        if self.currentQuestionIndex > 0:
            self.userPoints.set(self.display.get())

        if self.currentQuestionIndex < len(self.randomList):
            question_type = self.listeType[self.randomList[self.currentQuestionIndex]]
            if question_type in function:
                question_class = function[question_type]
                question_class()
            else:
                self.error()
                
            self.currentQuestionIndex += 1
        else:
            print("End quiz")
                    
    
    
    def Choice1(self):
        self.display = displayChoice1(self.master, self.play, 
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.listeType),
                                            playerPoint=self.userPoints.get(),
                                            style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def Choice2(self):
        self.display = displayChoice2(self.master, self.play, 
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.listeType),
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
                                           maxQuestion=len(self.listeType),
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
                                                 maxQuestion=len(self.listeType),
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
                                                 maxQuestion=len(self.listeType),
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
                                                 maxQuestion=len(self.listeType),
                                                 playerPoint=self.userPoints.get(),
                                                 style=self.user + 1)
        self.display.grid(row=0, column=0, sticky="nsew")


    def error(self):
        self.master.home()
        messagebox.showwarning("Erreur 20", "Une erreur s'est produite lors de la lecture du fichier de données des questions. Le fichier est peut être mal écrit, contient des erreurs ou est vide.")
