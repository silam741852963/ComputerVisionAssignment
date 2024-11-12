from PIL import Image
import numpy as np

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply an affine transformation with scaling, rotation, shear, and translation
def affine_transform(image, scale_x, scale_y, shear_x, shear_y, rotation_angle, translate_x, translate_y, output_path):
    # Convert rotation angle to radians
    angle_rad = rotation_angle * (np.pi / 180)  # degrees to radians
    
    # Affine transformation matrix combining scaling, rotation, shear, and translation
    matrix = (
        scale_x * np.cos(angle_rad) - shear_x * np.sin(angle_rad), 
        shear_y * np.cos(angle_rad) + scale_x * np.sin(angle_rad), 
        translate_x,
        shear_x * np.cos(angle_rad) - scale_y * np.sin(angle_rad),
        scale_y * np.cos(angle_rad) + shear_y * np.sin(angle_rad), 
        translate_y
    )
    
    transformed_image = image.transform(image.size, Image.AFFINE, matrix)
    transformed_image.save(output_path)
    return transformed_image

# Apply affine transformation with specific parameters and save image
affine_transform(
    image, 
    scale_x=1.2, scale_y=1.2,       # Scaling
    shear_x=0.2, shear_y=0.3,       # Shear factors
    rotation_angle=30,              # Rotation angle in degrees
    translate_x=5, translate_y=10, # Translation
    output_path='../image/affine_transformed_image.jpg'
)

print("Affine transformed image saved as 'affine_transformed_image.jpg'")
