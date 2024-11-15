from PIL import Image
import numpy as np

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)
width, height = image.size

# Convert the image to a numpy array for pixel manipulation
source_array = np.array(image)
destination_array = np.zeros_like(source_array)  # Create an empty array with the same shape as the source

# Define an affine transformation matrix for forward warping (e.g., scaling and translation)
affine_matrix = np.array([
    [1.2, 0.2, 30],  # Scaling x by 1.2, slight shear in y, and translation in x
    [0.1, 1.0, 20],  # Slight shear in x, scaling y by 1.0, and translation in y
])

# Forward warp function
def forward_warp(source, destination, matrix):
    src_height, src_width = source.shape[:2]
    
    for y in range(src_height):
        for x in range(src_width):
            # Apply the affine transformation to (x, y)
            new_pos = np.dot(matrix, [x, y, 1])
            new_x, new_y = int(new_pos[0]), int(new_pos[1])

            # Check if the new position is within the bounds of the destination image
            if 0 <= new_x < destination.shape[1] and 0 <= new_y < destination.shape[0]:
                destination[new_y, new_x] = source[y, x]  # Map pixel value

# Apply forward warping
forward_warp(source_array, destination_array, affine_matrix)

# Convert back to an image and save
destination_image = Image.fromarray(destination_array)
destination_image.save('../image/forward_warped_image.jpg')

print("Forward warped image saved as 'forward_warped_image.jpg'")
