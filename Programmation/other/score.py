from PIL import Image, ImageTk, ImageDraw
from pathlib import Path

paths = Path(__file__).parent.resolve()


class scoreApp:
    def __init__(self, score = [0, 0]):
        self.rouge = (148, 3, 3)
        self.bleu = (3, 3, 148)

        self.width = 250
        self.height = 40
        self.rayon = 17
        
        if score[0] == 0 and score[1] == 0:
            self.percentageRed = 50
        else:
            redScore = score[0] / (score[0] + score[1]) * 100
            if redScore > 93:
                self.percentageRed = 93
            elif redScore < 7:
                self.percentageRed = 7
            else:
                self.percentageRed = int(redScore)
        
        self.image = self.create_image()

    def create_image(self):
        image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))

        redImage = Image.new('RGB', (int(self.width * (self.percentageRed / 100)), self.height), self.rouge)
        redMask = Image.new('L', (int(self.width * (self.percentageRed / 100)), self.height), 0)
        draw = ImageDraw.Draw(redMask)
        draw.rectangle((self.rayon, 0, 
                        int(self.width * (self.percentageRed / 100)), self.height), 
                        fill=255)
        draw.rectangle((0, (self.height - (self.height / 2)) / 2, 
                        2 * self.rayon, (self.height + (self.height / 2)) / 2), 
                        fill=255)
        draw.pieslice((0, 0, 
                       2 * self.rayon, 2 * self.rayon), 
                       180, 270, fill=255)
        draw.pieslice((0, self.height - 2 * self.rayon, 
                       2 * self.rayon, self.height), 
                       90, 180, fill=255)
        redImage.putalpha(redMask)


        blueImage = Image.new('RGB', (int(self.width * (1 - (self.percentageRed / 100))), self.height), self.bleu)
        blueMask = Image.new('L', (int(self.width * (1 - (self.percentageRed / 100))), self.height), 0)
        draw = ImageDraw.Draw(blueMask)
        draw.rectangle((0, 0, 
                        int(self.width * (1 - (self.percentageRed / 100))) - self.rayon, self.height), 
                        fill=255)
        draw.rectangle((int(self.width * (1 - (self.percentageRed / 100))) - 2 * self.rayon, (self.height - (self.height / 2)) / 2, 
                        int(self.width * (1 - (self.percentageRed / 100))), (self.height + (self.height / 2)) / 2), 
                        fill=255)
        draw.pieslice((int(self.width * (1 - (self.percentageRed / 100))) - 2 * self.rayon, 0, 
                       int(self.width * (1 - (self.percentageRed / 100))), 2 * self.rayon), 
                       270, 0, fill=255)
        draw.pieslice((int(self.width * (1 - (self.percentageRed / 100))) - 2 * self.rayon, self.height - 2 * self.rayon, 
                       int(self.width * (1 - (self.percentageRed / 100))), self.height), 
                       0, 90, fill=255)
        blueImage.putalpha(blueMask)

        image.paste(redImage, (0, 0), redImage)
        image.paste(blueImage, (int(self.width * (self.percentageRed / 100)), 0), blueImage)


        borderImage = Image.open(paths / "../assets/quiz/Frame1.png")

        position = ((250 - borderImage.width) // 2, (40 - borderImage.height) // 2)
        image.paste(borderImage, position, borderImage)

        return image
    
    def get(self):
        return ImageTk.PhotoImage(self.image)