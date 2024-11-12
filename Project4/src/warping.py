from PIL import Image
import numpy as np

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply a shear warp transformation
def warp_image(image, shear_factor, output_path):
    width, height = image.size
    matrix = (1, shear_factor, 0, 0, 1, 0)  # Affine transformation matrix for shear
    warped_image = image.transform((width, height), Image.AFFINE, matrix)
    warped_image.save(output_path)
    return warped_image

# Apply shear warp with different factors and save images
warp_image(image, 0.2, '../image/warped_image_shear_0.2.jpg')   # Shear factor 0.2
warp_image(image, 0.5, '../image/warped_image_shear_0.5.jpg')   # Shear factor 0.5

print("Warped images saved as 'warped_image_shear_0.2.jpg' and 'warped_image_shear_0.5.jpg'")
