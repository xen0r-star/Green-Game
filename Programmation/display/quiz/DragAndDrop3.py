from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, ImageDraw
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

from other.chrono import ChronoApp
from other.score import scoreApp

paths = Path(__file__).parent.resolve()



class displayDragAndDrop3(Frame):
    """
    interface du quiz Partie 7 - Jeux a replacer les image dans la bonne catégorie
    """

    def __init__(self, master, callback, textQuestion, imageResponse, textZones, correctResponse, 
                 style=1, playerPoint=[0, 0], time=60, currentQuestion = 0, maxQuestion=20):
        super().__init__(master)
        self.callback = callback
        
        self.style = style
        self.time = time
        self.playerPoint = playerPoint

        self.textQuestion = textQuestion
        self.imageResponse = imageResponse
        self.textZones = textZones
        self.correctResponse = correctResponse

        self.questionNumber = f"{currentQuestion}/{maxQuestion}"
        self.response = [[0, 0] for _ in range(len(self.imageResponse))]
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
        self.photo = ImageTk.PhotoImage(Image.open(paths / "../../assets/quiz/zone.png"))
        self.canvas.create_image(620 // 2, 97, anchor=CENTER, image=self.photo)
        self.canvas.create_text(134, 18, text=self.textZones[0], font=("Arial", 15), anchor=N, fill="white")
        self.canvas.create_text(486, 18, text=self.textZones[1], font=("Arial", 15), anchor=N, fill="white")

        self.rectangles = []
        self.photoResponse = []
        for i in range(len(self.imageResponse)):
            src = paths / "../../data" / self.imageResponse[i]
            img = Image.open(src).convert("RGBA")
            draw = ImageDraw.Draw(img)
            width, height = img.size
            
            draw.rectangle([0, 0, width, 4], fill="white")
            draw.rectangle([0, 0, 4, height], fill="white")
            draw.rectangle([0, height-4, width, height], fill="white")
            draw.rectangle([width-4, 0, width, height], fill="white")

            photo = ImageTk.PhotoImage(img)
            self.photoResponse.append(photo)
            rect = self.canvas.create_image(84 + (117 * i), 220, anchor=NW, image=photo)

            DragDrop(self.canvas, rect, i+1, self.response, self.callbackPosition) 



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


    "Retourner la position"
    def callbackPosition(self, responce):
        self.response = responce

    "Valider et corriger la réponse"
    def validate(self):
        self.chrono.stop_timer()

        self.zones = {
            1: [76.0, 116.0],
            2: [193.0, 116.0],
            3: [427.0, 116.0],
            4: [544.0, 116.0]
        }

        a = 0
        for i in range(len(self.response)):
            if self.correctResponse[i] == 1:
                if self.response[i] == self.zones[1] or self.response[i] == self.zones[2]:
                    a += 1
            else:
                if self.response[i] == self.zones[3] or self.response[i] == self.zones[4]:
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
    
    def __init__(self, canvas, item, rect_id, response, callbackPosition):
        self.canvas = canvas
        self.item = item
        self.response = response
        self.rect_id = rect_id
        self.callbackPosition = callbackPosition
        self.magnetZone = [
            [26, 66, 126, 166],
            [143, 66, 243, 166],
            [377, 66, 477, 166],
            [494, 66, 594, 166]
        ]

        self.canvas.tag_bind(self.item, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.item, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.item, '<ButtonRelease-1>', self.on_release)
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
