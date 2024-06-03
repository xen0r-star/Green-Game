from tkinter import messagebox
from pathlib import Path
import random
from logzero import logger

from other.json.readJsonFile import readJsonFileSchema

from display.quiz.choice1 import displayChoice1
from display.quiz.choice2 import displayChoice2
from display.quiz.click1 import displayClick1
from display.quiz.DragAndDrop1 import displayDragAndDrop1
from display.quiz.DragAndDrop2 import displayDragAndDrop2
from display.quiz.DragAndDrop3 import displayDragAndDrop3
from display.score import displayScore


paths = Path(__file__).parent.resolve()


class solo:
    def __init__(self, master, numberQuestion):
        self.numberQuestion = numberQuestion
        self.master = master
        self.playerScore = 0

        self.readFile = readJsonFileSchema(paths / '../../data/question.json').get()
        if self.readFile == []:
            self.error()

        self.start()
        self.play()

    def start(self):
        self.listeType = []
        for data in self.readFile:
            self.listeType.append(data["type"])
        
        self.randomList = random.sample(range(0, len(self.listeType)), min(self.numberQuestion, len(self.listeType)))

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
            logger.info(f"End quiz, score player: {self.playerScore} ({int((self.playerScore / len(self.listeType)) * 100)})")

            displayScore(self.master, int((self.playerScore / len(self.listeType)) * 100))
                    
    
    
    def Choice1(self):
        self.display = displayChoice1(self.master, self.play, 
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.listeType),
                                            style=1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def Choice2(self):
        self.display = displayChoice2(self.master, self.play, 
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                            self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                            time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                            currentQuestion=self.currentQuestionIndex + 1,
                                            maxQuestion=len(self.listeType),
                                            style=1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def Click1(self):
        self.display = displayClick1(self.master, self.play, 
                                           self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                           self.readFile[self.randomList[self.currentQuestionIndex]]["answer"], 
                                           cursorStyle=self.readFile[self.randomList[self.currentQuestionIndex]]["cursor"],
                                           time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                           currentQuestion=self.currentQuestionIndex + 1,
                                           maxQuestion=len(self.listeType),
                                           style=1)
        self.display.grid(row=0, column=0, sticky="nsew")

    def DragAndDrop1(self):
        self.display = displayDragAndDrop1(self.master, self.play, 
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["question"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["choices"],
                                                 self.readFile[self.randomList[self.currentQuestionIndex]]["answer"],
                                                 time=self.readFile[self.randomList[self.currentQuestionIndex]]["time"],
                                                 currentQuestion=self.currentQuestionIndex + 1,
                                                 maxQuestion=len(self.listeType),
                                                 style=1)
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
                                                 style=1)
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
                                                 style=1)
        self.display.grid(row=0, column=0, sticky="nsew")


    def error(self):
        logger.error("Erreur 10")
        self.master.home()
        messagebox.showwarning("Erreur de lecture du fichier de données des questions", "Une erreur s'est produite lors de la lecture du fichier de données des questions. Le fichier est peut être mal écrit, contient des erreurs ou est vide.")
