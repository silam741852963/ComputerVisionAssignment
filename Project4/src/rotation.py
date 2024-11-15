from PIL import Image

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply rotation
def rotate_image(image, angle, output_path):
    rotated_image = image.rotate(angle, expand=True)  # Expand to fit the entire rotated image
    rotated_image.save(output_path)
    return rotated_image

# Apply rotation with different angles and save images
rotate_image(image, 45, '../image/rotated_image_45.jpg')  # Rotate by 45 degrees
rotate_image(image, 90, '../image/rotated_image_90.jpg')  # Rotate by 90 degrees

print("Rotated images saved as 'rotated_image_45.jpg' and 'rotated_image_90.jpg'")
