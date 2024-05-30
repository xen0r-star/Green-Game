from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

paths = Path(__file__).parent.resolve()



class displayChoice(Frame):
    def __init__(self, master, style=1):
        super().__init__(master)
        
        self.style = style
        self.questionNumberSelect = 0

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")
        self.addComponents()

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.grid_columnconfigure(0, weight=1)

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
                     text="Quel est le principal avantage des voitures électriques par rapport aux voitures à essence ?", 
                     fg=self.master.color_text, font=fontStyle, wraplength=600,
                     bg=self.master.color_background, 
                     width=625, height=100, 
                     column=0, row=1)
        
        fontStyle = font.Font(size=15, weight="bold")
        photo = ImageTk.PhotoImage(
            Image.open(paths / "../../assets/Frame6.png").resize((250, 40), Image.LANCZOS)
        )
        self.timer = Label(self.question, image=photo, text="00 : 00", compound="center", font=fontStyle, fg=self.master.color_text, bg=self.master.color_background)
        self.timer.image = photo
        self.timer.grid(column=0, row=2, pady=(7, 0))
        

        self.body = Frame(self, bg=self.master.color_background, height=325, width=620)
        self.body.grid(column=0, row=1)

        self.button_borders = []
        self.create_button_with_border(0, "Elles sont moins chères à l'achat.", 1)
        self.create_button_with_border(1, "Elles émettent moins de CO2.", 2)
        self.create_button_with_border(2, "Elles nécessitent moins d'entretien.", 3)
        self.create_button_with_border(3, "Elles ont une plus grande autonomie.", 4)


        custom_Button(self, 
                        command=self.validate, 
                        image=paths / "../../assets/quiz/valider.png",
                        height=75, width=343,
                        bg=self.master.color_background,
                        column=0, row=2, ipadx=5, ipady=2)
        

        fontStyle = font.Font(size=25, weight="bold")
        self.numberQuestion = Label(self, text="5/20", compound="center", font=fontStyle, fg=self.master.color_text2, bg=self.master.color_background)
        self.numberQuestion.grid(column=0, row=2, sticky=SE, padx=20, pady=20)


        ChronoApp(self.master, self.timer, 60)

    
    def create_button_with_border(self, row, text, button_number):
        buttonBorder = Frame(self.body, bg="white")
        buttonBorder.grid(column=0, row=row, pady=7)
        fontStyle = font.Font(size=15, weight="bold")
        button = Button(buttonBorder, text=text, font=fontStyle, justify='right', 
                           width=50, height=2,
                           fg=self.master.color_text, bg=self.master.color_fourth, bd=0, 
                           highlightthickness=4, highlightbackground="white", highlightcolor="white",
                           activebackground=self.master.color_fourth, activeforeground=self.master.color_text,
                           command=lambda: self.change_border_color(buttonBorder, button_number))
        button.grid(column=0, row=0, padx=5, pady=5)
        self.button_borders.append(buttonBorder)
    
    def change_border_color(self, selected_border, button_number):
        for border in self.button_borders:
            border.config(bg="white")

        selected_border.config(bg="#114232")
        self.questionNumberSelect = button_number
    

    def validate(self):
        print(self.questionNumberSelect)



class ChronoApp:
    def __init__(self, master, label, time):
        self.master = master
        self.label = label
        self.time_left = time
        self.update_timer()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label.config(text=self.format_time(self.time_left))
            self.master.after(1000, self.update_timer)