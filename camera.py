import cv2
from read import readQRCode

# Ouvrir le flux vidéo de la caméra
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Impossible d'ouvrir le flux vidéo")
    exit()

# Lire et afficher en continu le contenu de la caméra
while True:
    # Lire une image à partir du flux vidéo
    ret, frame = cap.read()

    # Vérifier si la lecture de l'image a réussi
    if not ret:
        print("Impossible de lire une image depuis le flux vidéo")
        break
    
    squares = readQRCode(frame)
    cv2.drawContours(frame, squares, -1, (0, 255, 0), 1)

    # # Afficher l'image capturée
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
