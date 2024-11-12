from PIL import Image

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply uniform scaling
def scale_image_uniform(image, scale_factor, output_path):
    width, height = image.size
    new_size = (int(width * scale_factor), int(height * scale_factor))
    scaled_image = image.resize(new_size)
    scaled_image.save(output_path)
    return scaled_image

# Function to apply non-uniform scaling
def scale_image_non_uniform(image, x_scale_factor, y_scale_factor, output_path):
    width, height = image.size
    new_size = (int(width * x_scale_factor), int(height * y_scale_factor))
    scaled_image = image.resize(new_size)
    scaled_image.save(output_path)
    return scaled_image

# Apply uniform scaling with different factors and save images
scale_image_uniform(image, 1.5, '../image/scaled_image_uniform_1.5.jpg')  # Uniform scaling by 1.5
scale_image_uniform(image, 0.5, '../image/scaled_image_uniform_0.5.jpg')  # Uniform scaling by 0.5

# Apply non-uniform scaling with different factors and save images
scale_image_non_uniform(image, 2.0, 0.5, '../image/scaled_image_non_uniform_2.0_0.5.jpg')  # x by 2.0, y by 0.5
scale_image_non_uniform(image, 0.5, 1.5, '../image/scaled_image_non_uniform_0.5_1.5.jpg')  # x by 0.5, y by 1.5

print("Scaled images saved as 'scaled_image_uniform_1.5.jpg', 'scaled_image_uniform_0.5.jpg', 'scaled_image_non_uniform_2.0_0.5.jpg', and 'scaled_image_non_uniform_0.5_1.5.jpg'")
