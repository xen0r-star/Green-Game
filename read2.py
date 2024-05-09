from PIL import Image, ImageDraw

# Charger l'image
image = Image.open('ImageChange.jpg')

# Convertir l'image en niveaux de gris
gray_image = image.convert('L')

# Définir le motif central caractéristique
pattern = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

# Définir la taille de la fenêtre de recherche
window_size = (len(pattern), len(pattern[0]))

draw = ImageDraw.Draw(image)

# Parcourir l'image avec une fenêtre glissante
for y in range(gray_image.height - window_size[0] + 1):
    for x in range(gray_image.width - window_size[1] + 1):
        # Extraire la région de l'image correspondant à la fenêtre
        window = gray_image.crop((x, y, x + window_size[1], y + window_size[0]))
        
        # Comparer la région avec le motif central
        if list(window.getdata()) == [pixel for row in pattern for pixel in row]:
            # Correspondance trouvée, enregistrer les coordonnées de la fenêtre
            print("Motif central trouvé aux coordonnées (x={}, y={})".format(x, y))
            draw.ellipse((x, y, x + window_size[1], y + window_size[0]), outline="red")

image.show()
