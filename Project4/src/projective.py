from PIL import Image
import numpy as np

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to compute the perspective transformation matrix
def compute_perspective_matrix(src_points, dst_points):
    matrix = []
    for p1, p2 in zip(src_points, dst_points):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1], -p2[0]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1], -p2[1]])
    matrix = np.array(matrix, dtype=np.float64)

    # Solve the matrix to find the perspective transformation coefficients
    _, _, V = np.linalg.svd(matrix)
    perspective_matrix = V[-1, :].reshape((3, 3))
    return perspective_matrix / perspective_matrix[2, 2]

# Function to apply perspective transformation
def perspective_transform(image, src_points, dst_points, output_path):
    width, height = image.size
    matrix = compute_perspective_matrix(src_points, dst_points).flatten()
    
    # Apply perspective transformation
    transformed_image = image.transform((width, height), Image.PERSPECTIVE, matrix, Image.BICUBIC)
    transformed_image.save(output_path)
    return transformed_image

# Define source points and destination points
src_points = [(0, 0), (image.width, 0), (image.width, image.height), (0, image.height)]  # Original corners
dst_points = [(0, 0), (image.width * 1.1, 50), (image.width * 0.9, image.height), (50, image.height * 0.8)]  # Skewed corners

# Apply perspective transformation and save image
perspective_transform(image, src_points, dst_points, '../image/perspective_transformed_image.jpg')

print("Perspective transformed image saved as 'perspective_transformed_image.jpg'")
