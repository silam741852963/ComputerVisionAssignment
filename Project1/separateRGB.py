from PIL import Image
import numpy as np

# Load the color image
img_color = np.array(Image.open('color_image.jpg'))

# Separate the color channels
R = img_color[:,:,0]
G = img_color[:,:,1]
B = img_color[:,:,2]

# Save each channel as a grayscale image
Image.fromarray(R).save('gray_R.jpg')
Image.fromarray(G).save('gray_G.jpg')
Image.fromarray(B).save('gray_B.jpg')