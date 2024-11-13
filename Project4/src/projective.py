from PIL import Image
import numpy as np

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to compute the projective transformation matrix
def compute_projective_matrix(src_points, dst_points):
    matrix = []
    for p1, p2 in zip(src_points, dst_points):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1], -p2[0]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1], -p2[1]])
    matrix = np.array(matrix, dtype=np.float64)

    # Solve the matrix to find the projective transformation coefficients
    _, _, V = np.linalg.svd(matrix)
    projective_matrix = V[-1, :].reshape((3, 3))
    return projective_matrix / projective_matrix[2, 2]

# Function to apply projective transformation
def projective_transform(image, src_points, dst_points, output_path):
    width, height = image.size
    matrix = compute_projective_matrix(src_points, dst_points).flatten()
    
    # Apply projective transformation
    transformed_image = image.transform((width, height), Image.PERSPECTIVE, matrix, Image.BICUBIC)
    transformed_image.save(output_path)
    return transformed_image

# Define source points and destination points
src_points = [(0, 0), (image.width, 0), (image.width, image.height), (0, image.height)]  # Original corners
dst_points = [(0, 0), (image.width * 0.6, 0), (image.width * 0.3, image.height), (0, image.height * 0.6)]  # Skewed corners

# Apply projective transformation and save image
projective_transform(image, src_points, dst_points, '../image/projective_transformed_image.jpg')

print("projective transformed image saved as 'projective_transformed_image.jpg'")
