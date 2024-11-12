from PIL import Image
import numpy as np
from scipy.ndimage import map_coordinates

# Load the forward-warped image
image_path = '../image/forward_warped_image.jpg'
warped_image = Image.open(image_path)
warped_array = np.array(warped_image)

# Define the forward affine transformation matrix
affine_matrix = np.array([
    [1.2, 0.2, 30],
    [0.1, 1.0, 20]
])

# Convert the 2x3 affine matrix to a 3x3 matrix for inversion
affine_matrix_3x3 = np.vstack([affine_matrix, [0, 0, 1]])
inverse_affine_matrix_3x3 = np.linalg.inv(affine_matrix_3x3)

# Extract the top 2 rows to use as the 2x3 inverse matrix
inverse_affine_matrix = inverse_affine_matrix_3x3[:2, :]

# Create an empty array for the destination image (original size)
destination_array = np.zeros_like(warped_array)

# Inverse warp function with interpolation
def inverse_warp(warped, destination, inverse_matrix):
    dst_height, dst_width, num_channels = destination.shape

    for y in range(dst_height):
        for x in range(dst_width):
            # Calculate the corresponding source coordinates in the warped image
            src_pos = np.dot(inverse_matrix, [x, y, 1])
            src_x, src_y = src_pos[0], src_pos[1]

            # Check if the source position is within the bounds of the warped image
            if 0 <= src_x < warped.shape[1] and 0 <= src_y < warped.shape[0]:
                # Use bilinear interpolation to get pixel values for each color channel
                for c in range(num_channels):
                    destination[y, x, c] = map_coordinates(
                        warped[:, :, c], [[src_y], [src_x]], order=1, mode='reflect'
                    )[0]

# Apply inverse warping to approximate the original image
inverse_warp(warped_array, destination_array, inverse_affine_matrix)

# Convert back to an image and save
inverse_image = Image.fromarray(destination_array)
inverse_image.save('../image/inverse_warped_image.jpg')

print("Inverse warped image saved as 'inverse_warped_image.jpg'")
