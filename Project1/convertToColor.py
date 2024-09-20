from PIL import Image
import numpy as np

# Load the grayscale images
gray_R = np.array(Image.open('gray_R.jpg'))
gray_G = np.array(Image.open('gray_G.jpg'))
gray_B = np.array(Image.open('gray_B.jpg'))

# Stack the grayscale images into a color image
img_color_reconstructed = np.stack([gray_R, gray_G, gray_B], axis=-1)

# Save the reconstructed color image
Image.fromarray(img_color_reconstructed.astype(np.uint8)).save('color_image_reconstructed.jpg')