from PIL import Image

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply shearing in the x or y direction
def shear_image(image, shear_factor, direction='x', output_path=None):
    width, height = image.size
    if direction == 'x':
        # Shear in the x-direction
        matrix = (1, shear_factor, 0, 0, 1, 0)
    elif direction == 'y':
        # Shear in the y-direction
        matrix = (1, 0, 0, shear_factor, 1, 0)
    else:
        raise ValueError("Direction must be 'x' or 'y'")

    sheared_image = image.transform((width, height), Image.AFFINE, matrix)
    if output_path:
        sheared_image.save(output_path)
    return sheared_image

# Apply shearing in the x and y directions and save images
shear_image(image, 0.3, 'x', '../image/sheared_image_x_0.3.jpg')  # Shear in x-direction with factor 0.3
shear_image(image, 0.3, 'y', '../image/sheared_image_y_0.3.jpg')  # Shear in y-direction with factor 0.3

print("Sheared images saved as 'sheared_image_x_0.3.jpg' and 'sheared_image_y_0.3.jpg'")
