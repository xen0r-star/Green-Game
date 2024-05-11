import cv2
import numpy as np

def sauvola_binarization(image, taille_bloc, k, R):
    # niveau de gris
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape

    pixels = np.array(gray_image) # Convertir l'image en tableau NumPy
    binarized_pixels = np.zeros((height, width), dtype=np.uint8) # Créer une matrice pour stocker les pixels binarisés

    for y in range(0, height, taille_bloc): # Parcourir chaque bloc dans l'image
        for x in range(0, width, taille_bloc):
            # Extraire le bloc
            bloc = pixels[y:y+taille_bloc, x:x+taille_bloc]

            # Calculer la moyenne et l'écart-type du bloc
            mean = np.mean(bloc)
            std_dev = np.std(bloc)

            seuil = mean * (1 + k * ((std_dev / R) - 1)) # Calculer le seuil de Sauvola
            bloc_binarise = (bloc > seuil) * 255 # Binariser le bloc en utilisant le seuil de Sauvola

            binarized_pixels[y:y+taille_bloc, x:x+taille_bloc] = bloc_binarise # Coller le bloc binarisé dans la matrice binarisée

    return binarized_pixels

def angle_cos(A, B, C):
    BA = A - B
    BC = C - B
    dot_product = np.dot(BA, BC)
    norm_AB = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)
    angle_cos = dot_product / (norm_AB * norm_BC)
    return angle_cos

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # print(img)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    #print(cnt)
                    a = (cnt[1][1] - cnt[0][1])

                    if max_cos < 0.1 and a < img.shape[0]*0.8:

                        squares.append(cnt)
    return squares

def readQRCode(image):
    matrix_binarisee = sauvola_binarization(image, taille_bloc=20, k=0.2, R=128)
    squares = find_squares(matrix_binarisee)

    return squares