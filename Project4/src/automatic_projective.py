import cv2
import numpy as np

# Paths to images
keanu_path = '../image/keanu_reeves.jpg'
rect1_path = '../image/khung_chu_nhat_1.jpg'
rect2_path = '../image/khung_chu_nhat_2.jpg'

# Load images
keanu_img = cv2.imread(keanu_path)
rect1_img = cv2.imread(rect1_path)
rect2_img = cv2.imread(rect2_path)

# Function to find the largest rectangle in the image larger than a certain area threshold
def find_large_rectangle(img, area_threshold):
    # Convert to grayscale and apply edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store the largest rectangle
    largest_rect = None
    largest_area = 0

    # Iterate through contours to find the largest rectangle
    for contour in contours:
        # Approximate the contour
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour is a rectangle (4 corners) and meets the area threshold
        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > area_threshold and area > largest_area:
                largest_rect = approx
                largest_area = area

    # Return the largest rectangle points if found
    if largest_rect is not None:
        return np.float32([point[0] for point in largest_rect])
    else:
        return None

# Function to apply projective transformation using the found rectangle
def projective_transform_with_rectangle(target_img, src_img, area_threshold):
    # Find the largest rectangle in the target image
    rect_points = find_large_rectangle(target_img, area_threshold)
    if rect_points is None:
        print("No rectangle found that meets the area threshold.")
        return target_img

    # Define source points (corners of the Keanu image)
    keanu_height, keanu_width = src_img.shape[:2]
    keanu_points = np.float32([[0, 0], [keanu_width, 0], [keanu_width, keanu_height], [0, keanu_height]])

    # Compute the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(keanu_points, rect_points)

    # Warp the source image to fit the detected rectangle
    warped_image = cv2.warpPerspective(src_img, matrix, (target_img.shape[1], target_img.shape[0]))

    # Create a mask for the warped area
    mask = np.zeros_like(target_img, dtype=np.uint8)
    cv2.fillConvexPoly(mask, np.int32(rect_points), (255, 255, 255))

    # Blend the warped image into the target image using the mask
    masked_target = cv2.bitwise_and(target_img, cv2.bitwise_not(mask))
    blended_image = cv2.add(masked_target, cv2.bitwise_and(warped_image, mask))

    return blended_image

# Set an area threshold
area_threshold = 1000 

# Apply the projective transformation on both rectangle images
rect1_auto_blended = projective_transform_with_rectangle(rect1_img, keanu_img, area_threshold)
rect2_auto_blended = projective_transform_with_rectangle(rect2_img, keanu_img, area_threshold)

# Save the automatically transformed images
cv2.imwrite('../image/auto_blended_image_1.jpg', rect1_auto_blended)
cv2.imwrite('../image/auto_blended_image_2.jpg', rect2_auto_blended)

print("Automatic blended images saved as 'auto_blended_image_1.jpg' and 'auto_blended_image_2.jpg'")
