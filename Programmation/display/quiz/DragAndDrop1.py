from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

from other.chrono import ChronoApp
from other.score import scoreApp

paths = Path(__file__).parent.resolve()



class displayDragAndDrop1(Frame):
    """
    interface du quiz Partie 5 - Jeux a replacer les textes sur la ligne du temps
    """

    def __init__(self, master, callback, textQuestion, textResponse, correctResponse, 
                 style=1, playerPoint=[0, 0], time=60, currentQuestion = 0, maxQuestion=20):
        super().__init__(master)
        self.callback = callback
        
        self.style = style
        self.time = time
        self.playerPoint = playerPoint

        self.textQuestion = textQuestion
        self.textResponse = textResponse
        self.correctResponse = correctResponse

        self.questionNumber = f"{currentQuestion}/{maxQuestion}"
        self.response = [[0, 0] for _ in range(len(self.textResponse))]
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

        self.canvas = Canvas(self.body, height=325, width=620, bg=self.master.color_background, bd=0, highlightthickness=0)
        self.canvas.grid(column=0, row=0)
        self.photo = ImageTk.PhotoImage(Image.open(paths / "../../assets/quiz/timeLine.png"))
        self.canvas.create_image(620 // 2, 97, anchor=CENTER, image=self.photo)

        self.rectangles = []
        for i in range(len(self.textResponse)):
            rect = self.canvas.create_rectangle(
                26 + (117 * i), 220, 26 + (117 * i) + 100, 220 + 100, 
                fill=self.master.color_fourth, outline="#FFFFFF", width=4
            )
            text_items = self.create_wrapped_text(26 + (117 * i) + 5, 220 + 3, self.textResponse[i], max_width=90)
            self.rectangles.append((rect, text_items))
            DragDrop(self.canvas, rect, text_items, i+1, self.response, self.callbackPosition) 


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
    

    "Divise le texte en plusieur partie pour pas dépasser le cadre"
    def create_wrapped_text(self, x, y, text, max_width):
        words = text.split()
        lines = []
        line = ""
        text_items = []

        for word in words:
            test_line = f"{line} {word}".strip()
            temp_text_item = self.canvas.create_text(x, y, text=test_line, font=("Arial", 12), anchor=NW, fill="white")
            bbox = self.canvas.bbox(temp_text_item)
            self.canvas.delete(temp_text_item)

            if bbox[2] - bbox[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        
        lines.append(line)
        for i, line in enumerate(lines):
            text_item = self.canvas.create_text(x, y + i * 15, text=line, fill="white", font=("Arial", 12), anchor=NW)
            text_items.append(text_item)

        return text_items
    

    "Retourner la position"
    def callbackPosition(self, responce):
        self.response = responce

    "Valider et corriger la réponse"
    def validate(self):
        if self.style != 2 and self.style != 3:
            self.chrono.stop_timer()

        self.zones = {
            1: [76.0, 116.0],
            2: [193.0, 116.0],
            3: [310.0, 116.0],
            4: [427.0, 116.0],
            5: [544.0, 116.0]
        }

        a = 0
        for i in range(len(self.response)):
            if self.response[i] == self.zones[self.correctResponse[i]]:
                a += 1

        if a == len(self.response):
            self.points = 1
        
        if self.callback:
            self.callback()
    
    "Retourner le score"
    def get(self):
        return self.points



class DragDrop:
    """
    Permet le mouvements des éléments
    """
    
    def __init__(self, canvas, item, text_items, rect_id, response, callbackPosition):
        self.canvas = canvas
        self.item = item
        self.response = response
        self.text_items = text_items
        self.rect_id = rect_id
        self.callbackPosition = callbackPosition
        self.magnetZone = [
            [26, 66, 126, 166],
            [143, 66, 243, 166],
            [260, 66, 360, 166],
            [377, 66, 477, 166],
            [494, 66, 594, 166]
        ]

        self.canvas.tag_bind(self.item, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.item, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.item, '<ButtonRelease-1>', self.on_release)
        for text_item in self.text_items:
            self.canvas.tag_bind(text_item, '<ButtonPress-1>', self.on_press)
            self.canvas.tag_bind(text_item, '<B1-Motion>', self.on_drag)
            self.canvas.tag_bind(text_item, '<ButtonRelease-1>', self.on_release)
        self.is_magnetized = False

    def on_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y

        x1, y1, x2, y2 = self.canvas.bbox(self.item)
        if x1 + dx < 0 or y1 + dy < 0 or x2 + dx > 620 or y2 + dy > 325:
            return

        self.canvas.move(self.item, dx, dy)
        for text_item in self.text_items:
            self.canvas.move(text_item, dx, dy)
        self.x = event.x
        self.y = event.y
        self.check_magnet()

    def on_release(self, event):
        self.x = event.x
        self.y = event.y
        self.check_magnet(release=True)
        self.update_position()

    def check_magnet(self, release=False):
        x1, y1, x2, y2 = self.canvas.bbox(self.item)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        for zone in self.magnetZone:
            zx1, zy1, zx2, zy2 = zone
            zcx = (zx1 + zx2) / 2
            zcy = (zy1 + zy2) / 2

            if abs(cx - zcx) < 10 and abs(cy - zcy) < 10:
                if not release:
                    dx = zcx - cx
                    dy = zcy - cy

                    if x1 + dx < 0 or y1 + dy < 0 or x2 + dx > 620 or y2 + dy > 325:
                        return
                    
                    self.canvas.move(self.item, dx, dy)
                    for text_item in self.text_items:
                        self.canvas.move(text_item, dx, dy)
                    self.is_magnetized = True
                return

            if release:
                if abs(cx - zcx) > 30 or abs(cy - zcy) > 30:
                    self.is_magnetized = False
                return
    
    def update_position(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.item)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        self.response[self.rect_id - 1] = [cx, cy]
        self.callbackPosition(self.response)
