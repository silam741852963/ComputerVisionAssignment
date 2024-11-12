from PIL import Image

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply mirroring (reflection) across x or y axis
def mirror_image(image, axis, output_path):
    if axis == 'x':
        mirrored_image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Reflect across x-axis (vertical flip)
    elif axis == 'y':
        mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)  # Reflect across y-axis (horizontal flip)
    else:
        raise ValueError("Axis must be 'x' or 'y'")

    mirrored_image.save(output_path)
    return mirrored_image

# Apply mirroring across x and y axes and save images
mirror_image(image, 'x', '../image/mirrored_image_x.jpg')  # Reflection across x-axis
mirror_image(image, 'y', '../image/mirrored_image_y.jpg')  # Reflection across y-axis

print("Mirrored images saved as 'mirrored_image_x.jpg' and 'mirrored_image_y.jpg'")
