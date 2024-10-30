import cv2
import numpy as np

def add_mask_padding(mask, padding=10):
    """
    Add padding to the binary mask to avoid ghosting effects.
    Arguments:
        mask -- Binary mask defining the object area (same size as the source)
        padding -- Number of pixels to expand the mask (default is 10)
    Returns:
        Padded mask with the same size as the input mask.
    """
    kernel = np.ones((padding, padding), np.uint8)
    padded_mask = cv2.dilate(mask, kernel, iterations=1)  # Expand the mask area
    return padded_mask

def poisson_blend(source, target, mask, offset=(0, 0)):
    """
    Perform Poisson blending to insert source image object into the target image.
    Arguments:
        source -- Object image (foreground) with alpha channel
        target -- Background image
        mask -- Binary mask defining object area (same size as source)
        offset -- (x, y) offset for placing the source into the target
    """
    # Calculate the region where the object will be placed in the target
    x_offset, y_offset = offset
    y1, y2 = y_offset, y_offset + source.shape[0]
    x1, x2 = x_offset, x_offset + source.shape[1]

    # Perform Poisson blending using seamlessClone from OpenCV
    blended = cv2.seamlessClone(
        source, target, mask, (x_offset + source.shape[1] // 2, y_offset + source.shape[0] // 2), cv2.MIXED_CLONE
    )

    return blended

# Load the uploaded images (ensure the object image has an alpha channel)
background = cv2.imread('../image/background.jpg')
object_img = cv2.imread('../image/object.png', cv2.IMREAD_UNCHANGED)  # Load with alpha channel

# Resize object to better fit into the room's corner (optional)
object_img = cv2.resize(object_img, (200, 267))

# Separate color channels and alpha channel from the object image
b, g, r, alpha = cv2.split(object_img)

# Merge only the RGB channels back into the object image
object_rgb = cv2.merge([b, g, r])

# Create a mask based on the alpha channel (1 where alpha > 0, 0 elsewhere)
mask = np.where(alpha > 0, 255, 0).astype(np.uint8)

# Add padding to the mask to avoid ghosting effects
padded_mask = add_mask_padding(mask, padding=15)

# Offset to place the object in the bottom-left corner of the room
offset = (350, 550)

# Perform Poisson blending
result = poisson_blend(object_rgb, background, padded_mask, offset=offset)

# Save the result
cv2.imwrite('../image/blended_result.jpg', result)
