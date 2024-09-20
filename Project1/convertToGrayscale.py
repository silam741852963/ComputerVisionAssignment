from PIL import Image
import numpy as np

# Load the color image
img_color = np.array(Image.open('color_image.jpg'))

# Convert the color image to grayscale using weighted sum
img_gray = 0.2989 * img_color[:,:,0] + 0.5870 * img_color[:,:,1] + 0.1140 * img_color[:,:,2]

# Save the grayscale image
Image.fromarray(img_gray.astype(np.uint8)).save('gray_image.jpg')