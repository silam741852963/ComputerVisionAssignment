import numpy as np
from PIL import Image

# Apply the filter to a single color channel
def apply_filter(image_channel, kernel):
    img_height, img_width = image_channel.shape
    kernel_size = kernel.shape[0]
    pad_size = kernel_size // 2
    padded_image = np.pad(image_channel, pad_size, mode='constant')
    filtered_image = np.zeros_like(image_channel)

    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i+kernel_size, j:j+kernel_size]
            filtered_image[i, j] = np.sum(region * kernel)

    return filtered_image

# Laplacian Kernel for High-Pass Filtering
laplacian_kernel = np.array([[-1, -1, -1],
                             [-1,  8, -1],
                             [-1, -1, -1]])

# Load the image
img = Image.open('image/image.jpg')
img_array = np.array(img)

# Separate the image into R, G, B channels
r_channel = img_array[:, :, 0]
g_channel = img_array[:, :, 1]
b_channel = img_array[:, :, 2]

# Apply the Laplacian filter to each color channel
r_filtered = apply_filter(r_channel, laplacian_kernel)
g_filtered = apply_filter(g_channel, laplacian_kernel)
b_filtered = apply_filter(b_channel, laplacian_kernel)

# Stack the filtered channels back into a color image
filtered_img_array = np.stack([r_filtered, g_filtered, b_filtered], axis=-1)

# Convert back to uint8 and save the result
filtered_img = Image.fromarray(np.clip(filtered_img_array, 0, 255).astype(np.uint8))
filtered_img.save('image/high_pass_image.jpg')
