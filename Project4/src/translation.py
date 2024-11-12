from PIL import Image

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply translation
def translate_image(image, x_offset, y_offset, output_path):
    width, height = image.size
    matrix = (1, 0, x_offset, 0, 1, y_offset)  # Affine transformation matrix for translation
    translated_image = image.transform((width, height), Image.AFFINE, matrix)
    translated_image.save(output_path)
    return translated_image

# Apply translation with different offsets and save images
translate_image(image, 50, 20, '../image/translated_image_50_20.jpg')  # Translate by (50, 20) pixels
translate_image(image, -30, -15, '../image/translated_image_-30_-15.jpg')  # Translate by (-30, -15) pixels

print("Translated images saved as 'translated_image_50_20.jpg' and 'translated_image_-30_-15.jpg'")
