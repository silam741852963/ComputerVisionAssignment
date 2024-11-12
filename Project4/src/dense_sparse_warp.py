import cv2
import numpy as np
from PIL import Image
from scipy.interpolate import griddata

# Load the image
image_path = '../image/okita.png'
image = Image.open(image_path).convert('RGB')
image_array = np.array(image)
height, width = image_array.shape[:2]

### Dense Warp Specification

# Create a dense vector field (for demonstration, let's make a swirl effect)
def create_dense_vector_field(height, width):
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    x_center, y_center = width // 2, height // 2
    angle = np.arctan2(y - y_center, x - x_center)
    radius = np.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)
    # Apply a swirl effect based on radius
    x_displacement = radius * np.cos(angle + radius * 0.01)
    y_displacement = radius * np.sin(angle + radius * 0.01)
    return x + x_displacement, y + y_displacement

# Apply dense warp to the image
def dense_warp(image_array, x_field, y_field):
    map_x = np.float32(x_field)
    map_y = np.float32(y_field)
    warped_image = cv2.remap(image_array, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return warped_image

# Create the dense vector field and apply warp
x_field, y_field = create_dense_vector_field(height, width)
dense_warped_image = dense_warp(image_array, x_field, y_field)
dense_warped_image_pil = Image.fromarray(dense_warped_image)
dense_warped_image_pil.save('../image/dense_warped_image.jpg')

print("Dense warped image saved as 'dense_warped_image.jpg'")


### Sparse Warp Specification

# Define sparse key points for transformation
# Example feature points (you can detect these using feature detectors like SIFT in practice)
points_src = np.array([[100, 100], [400, 100], [100, 400], [400, 400]])
points_dst = np.array([[120, 120], [420, 80], [90, 380], [390, 420]])

# Interpolate the transformation for sparse warp
def sparse_warp(image_array, points_src, points_dst):
    # Generate a grid of coordinates covering the image
    grid_x, grid_y = np.meshgrid(np.arange(width), np.arange(height))
    grid_coords = np.vstack([grid_x.ravel(), grid_y.ravel()]).T

    # Compute the transformations for each point
    points_transformed = griddata(points_src, points_dst - points_src, grid_coords, method='linear', fill_value=0)
    points_transformed = points_transformed.reshape(height, width, 2)

    # Apply the transformations
    map_x = (grid_x + points_transformed[..., 0]).astype(np.float32)
    map_y = (grid_y + points_transformed[..., 1]).astype(np.float32)
    sparse_warped_image = cv2.remap(image_array, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return sparse_warped_image

# Apply sparse warp to the image
sparse_warped_image = sparse_warp(image_array, points_src, points_dst)
sparse_warped_image_pil = Image.fromarray(sparse_warped_image)
sparse_warped_image_pil.save('../image/sparse_warped_image.jpg')

print("Sparse warped image saved as 'sparse_warped_image.jpg'")
