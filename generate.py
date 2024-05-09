from PIL import Image, ImageDraw


def generateQRCode(id, nameImage = "QRCode"):
    id = [[int(digit) for digit in bin(ord(idBin)).replace("b", "").zfill(8)] for idBin in str(id)] # 48 => [[0, 0, 1, 1, 0, 1, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0]]
    print(id)

    pxSize = 20
    structure = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    for a in range(4):
        structure = [list(row) for row in zip(*structure[::-1])] # 90 degree rotation of the matrix
        
        for b in range(0, 8, 2):
            structure[b // 2][2] = id[0][b]
            structure[b // 2][3] = id[0][b + 1]
            structure[b // 2][4] = id[1][b]
            structure[b // 2][5] = id[1][b + 1]

    image = Image.new("RGB", (20 * pxSize, 20 * pxSize), "white")
    draw = ImageDraw.Draw(image)

    draw.rectangle([(pxSize * 2, pxSize * 2), (pxSize * 2 + pxSize * 16, pxSize * 2 + pxSize * 16)], fill = "black")

    for a, b in enumerate(structure):
        for c, d in enumerate(b):
            if d == 1:
                color = "black"
            else:
                color = "white"

            draw.rectangle([(c * pxSize + pxSize * 3, a * pxSize + pxSize * 3), ((c * pxSize + pxSize * 4) - 1, (a * pxSize + pxSize * 4) - 1)], fill=color)

    image.save(f"{nameImage}.png")

generateQRCode("15")