import cv2
import numpy as np

# Load images
keanu_path = '../image/keanu_reeves.jpg'
rect1_path = '../image/khung_chu_nhat_1.jpg'
rect2_path = '../image/khung_chu_nhat_2.jpg'

keanu_img = cv2.imread(keanu_path)
rect1_img = cv2.imread(rect1_path)
rect2_img = cv2.imread(rect2_path)

# Resize the Keanu image to match the target rectangle sizes
keanu_height, keanu_width = keanu_img.shape[:2]
keanu_points = np.float32([[0, 0], [keanu_width, 0], [keanu_width, keanu_height], [0, keanu_height]])

# Define destination points for manual transformation on rect1 and rect2 images
# Adjust coordinates as needed
dst_points1 = np.float32([[1055, 605], [2080, 1009], [2035, 2728], [842, 2654]])
dst_points2 = np.float32([[1221, 481], [2000, -390], [2064, 3780], [559, 3724]])

# Function to apply projective transformation
def projective_transform(target_img, src_img, src_points, dst_points):
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_image = cv2.warpPerspective(src_img, matrix, (target_img.shape[1], target_img.shape[0]))
    
    mask = np.zeros_like(target_img, dtype=np.uint8)
    cv2.fillConvexPoly(mask, np.int32(dst_points), (255, 255, 255))
    
    masked_target = cv2.bitwise_and(target_img, cv2.bitwise_not(mask))
    blended_image = cv2.add(masked_target, cv2.bitwise_and(warped_image, mask))
    
    return blended_image

# Apply the transformation manually
rect1_manual_blended = projective_transform(rect1_img, keanu_img, keanu_points, dst_points1)
rect2_manual_blended = projective_transform(rect2_img, keanu_img, keanu_points, dst_points2)

# Save the manually transformed images
cv2.imwrite('../image/manual_blended_image_1.jpg', rect1_manual_blended)
cv2.imwrite('../image/manual_blended_image_2.jpg', rect2_manual_blended)

print("Manual blended images saved as 'manual_blended_image_1.jpg' and 'manual_blended_image_2.jpg'")
