from tkinter import *

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("Relier les rectangles")
        self.geometry("620x325")
        
        self.canvas = Canvas(self, width=620, height=325, bg="lightpink")
        self.canvas.pack()

        # Création des rectangles et du texte à l'intérieur
        self.rectangles = []
        self.rect_text_map = {}  # Map rectangle ID to text ID
        
        for i in range(3):
            rect_g = self.canvas.create_rectangle(10, i * 113 + 6, 200, 100 + i * 113 - 6, fill="lightblue", outline="White", width=6)
            text_g = self.canvas.create_text(10 + 100, i * 113 + 50, text=f"Rectangle G{i+1}", anchor=CENTER)
            self.rectangles.append(rect_g)
            self.rect_text_map[rect_g] = text_g

            rect_d = self.canvas.create_rectangle(414, i * 113 + 6, 414 + 200, 100 + i * 113 - 6, fill="lightblue", outline="White", width=6)
            text_d = self.canvas.create_text(414 + 100, i * 113 + 50, text=f"Rectangle G{i+1}", anchor=CENTER)

            self.rectangles.append(rect_d)
            self.rect_text_map[rect_d] = text_d

        # Ajout des événements pour les connexions
        self.canvas.bind("<Button-1>", self.on_click)
        self.selected_rect = None

    def on_click(self, event):
        # Détection du rectangle cliqué ou du texte associé
        item = self.canvas.find_closest(event.x, event.y)
        if item and item[0] in self.rectangles or item[0] in self.rect_text_map.values():
            rect = item[0]
            if rect in self.rect_text_map.values():
                rect = list(self.rect_text_map.keys())[list(self.rect_text_map.values()).index(rect)]
            if self.selected_rect:
                if self.selected_rect != rect:
                    # Dessiner la ligne entre les deux rectangles
                    x1, y1, x2, y2 = self.canvas.coords(self.selected_rect)
                    x1_centre = (x1 + x2) / 2
                    y1_centre = (y1 + y2) / 2

                    x3, y3, x4, y4 = self.canvas.coords(rect)
                    x2_centre = (x3 + x4) / 2
                    y2_centre = (y3 + y4) / 2

                    self.canvas.create_line(x1_centre, y1_centre, x2_centre, y2_centre, fill="black")

                    # Réinitialiser les bordures des rectangles
                    self.canvas.itemconfig(self.selected_rect, outline="black")
                    self.canvas.itemconfig(rect, outline="black")
                    self.selected_rect = None
                else:
                    # Désélectionner le même rectangle si cliqué deux fois
                    self.canvas.itemconfig(self.selected_rect, outline="black")
                    self.selected_rect = None
            else:
                # Sélectionner le rectangle
                self.selected_rect = rect
                self.canvas.itemconfig(self.selected_rect, outline="red")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
