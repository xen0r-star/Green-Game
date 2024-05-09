from PIL import Image, ImageFilter

file = "Image.jpg"
image = Image.open(file)

# Canny filter
gray = image.convert('L') # Convert the image to greyscale
blurred = gray.filter(ImageFilter.GaussianBlur(radius=2)) # Apply Gaussian blur to reduce noise
image = blurred.filter(ImageFilter.FIND_EDGES) # Apply the Canny filter to detect contours


image.save("ImageChange.jpg")