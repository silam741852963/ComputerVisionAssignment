from PIL import Image
import numpy as np

# Load the rotated image
rotated_image_path = '../image/rotated_image_45.jpg'
rotated_image = Image.open(rotated_image_path)
rotated_array = np.array(rotated_image)
height, width = rotated_array.shape[:2]

# Create an empty array for the restored image
restored_array = np.zeros_like(rotated_array)

# Define the inverse rotation matrix (for a 45-degree rotation)
angle_rad = -45 * (np.pi / 180)  # Inverse of 45 degrees in radians
cos_theta, sin_theta = np.cos(angle_rad), np.sin(angle_rad)
inverse_rotation_matrix = np.array([
    [cos_theta, -sin_theta],
    [sin_theta, cos_theta]
])

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
for y in range(height):
    for x in range(width):
        # Center the coordinates around the image center
        centered_x, centered_y = x - width // 2, y - height // 2

        # Apply the inverse rotation transformation
        src_x, src_y = np.dot(inverse_rotation_matrix, [centered_x, centered_y])

        # Shift the coordinates back to the original image position
        src_x += width // 2
        src_y += height // 2

        # If the source position is within bounds, apply bilinear interpolation
        if 0 <= src_x < width and 0 <= src_y < height:
            restored_array[y, x] = bilinear_interpolate(rotated_array, src_x, src_y)

# Convert back to an image and save
restored_image = Image.fromarray(restored_array.astype('uint8'))
restored_image.save('../image/restored_image.jpg')

print("Restored image saved as 'restored_image.jpg'")