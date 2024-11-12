from PIL import Image
import numpy as np

# Load the rotated image
rotated_image_path = '../image/rotated_image_45.jpg'
rotated_image = Image.open(rotated_image_path)
rotated_array = np.array(rotated_image)
height, width = rotated_array.shape[:2]

# Calculate new dimensions to fit the original unrotated image
diag_length = int(np.sqrt(width**2 + height**2))  # Diagonal of the bounding box
new_width, new_height = diag_length, diag_length

# Create an empty array for the expanded restored image
expanded_restored_array = np.zeros((new_height, new_width, 3), dtype=rotated_array.dtype)

# Define the inverse rotation matrix (for a 45-degree rotation)
angle_rad = -45 * (np.pi / 180)  # Inverse of 45 degrees in radians
cos_theta, sin_theta = np.cos(angle_rad), np.sin(angle_rad)
inverse_rotation_matrix = np.array([
    [cos_theta, -sin_theta],
    [sin_theta, cos_theta]
])

# Calculate the offset to center the rotated image on the expanded canvas
offset_x = (new_width - width) // 2
offset_y = (new_height - height) // 2

# Function to perform bilinear interpolation
def bilinear_interpolate(img, x, y):
    x0, y0 = int(np.floor(x)), int(np.floor(y))
    x1, y1 = min(x0 + 1, img.shape[1] - 1), min(y0 + 1, img.shape[0] - 1)
    dx, dy = x - x0, y - y0

    # Interpolate the pixel values
    top = (1 - dx) * img[y0, x0] + dx * img[y0, x1]
    bottom = (1 - dx) * img[y1, x0] + dx * img[y1, x1]
    value = (1 - dy) * top + dy * bottom
    return value

# Inverse warping process
for y in range(new_height):
    for x in range(new_width):
        # Offset coordinates to center the rotation
        centered_x, centered_y = x - new_width // 2, y - new_height // 2

        # Apply the inverse rotation transformation
        src_x, src_y = np.dot(inverse_rotation_matrix, [centered_x, centered_y])

        # Shift the coordinates back to the original image space
        src_x += width // 2
        src_y += height // 2

        # If the source position is within bounds, apply bilinear interpolation
        if 0 <= src_x < width and 0 <= src_y < height:
            expanded_restored_array[y, x] = bilinear_interpolate(rotated_array, src_x, src_y)

# Convert back to an image and save
expanded_restored_image = Image.fromarray(expanded_restored_array.astype('uint8'))
expanded_restored_image.save('../image/expanded_restored_image.jpg')

print("Expanded restored image saved as 'expanded_restored_image.jpg'")
