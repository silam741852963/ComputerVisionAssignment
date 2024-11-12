import cv2
import numpy as np
from PIL import Image
from scipy.spatial import Delaunay

# Load the two images
image_path1 = '../image/okita.png'
image_path2 = '../image/kohaku.png'
image1 = Image.open(image_path1).convert('RGB')  # Convert to RGB to remove alpha channel
image2 = Image.open(image_path2).convert('RGB')  # Convert to RGB to remove alpha channel

# Resize images to the same size if they are different
width = min(image1.width, image2.width)
height = min(image1.height, image2.height)
image1 = np.array(image1.resize((width, height)))
image2 = np.array(image2.resize((width, height)))

# Example feature points manually defined for simplicity
points1 = np.array([[100, 100], [400, 100], [250, 400], [150, 300], [350, 300]])
points2 = np.array([[120, 120], [420, 90], [260, 390], [160, 320], [370, 280]])

# Perform Delaunay triangulation on the points in the first image
tri = Delaunay(points1)

# Function to warp a single triangle
def warp_triangle(img1, img2, t1, t2):
    # Calculate bounding boxes for the triangles
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by the bounding box top-left corner
    t1_offset = [(pt[0] - r1[0], pt[1] - r1[1]) for pt in t1]
    t2_offset = [(pt[0] - r2[0], pt[1] - r2[1]) for pt in t2]

    # Crop the triangular regions
    img1_cropped = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.uint8)
    cv2.fillConvexPoly(mask, np.int32(t2_offset), (1, 1, 1))

    # Compute the affine transform
    matrix = cv2.getAffineTransform(np.float32(t1_offset), np.float32(t2_offset))

    # Apply affine transformation to the triangular region
    img2_cropped = cv2.warpAffine(img1_cropped, matrix, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    img2_cropped = img2_cropped * mask

    # Copy the warped triangle to the output image
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (1 - mask) + img2_cropped

# Apply the warping on each triangle
warped_image = np.copy(image2)
for simplex in tri.simplices:
    # Get the corresponding triangles in both images
    t1 = points1[simplex]
    t2 = points2[simplex]

    # Warp the triangle from image1 to image2
    warp_triangle(image1, warped_image, t1, t2)

# Save the result
warped_image_pil = Image.fromarray(warped_image)
warped_image_pil.save('../image/local_warped_image.jpg')

print("Local warped image saved as 'local_warped_image.jpg'")
