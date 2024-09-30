import numpy as np
from PIL import Image

# Gaussian Kernel Generation Function
def gaussian_kernel(size, sigma):
    kernel = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            x = i - center
            y = j - center
            kernel[i, j] = (1 / (2 * np.pi * sigma**2)) * np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return kernel / np.sum(kernel)

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

# Load the image
img = Image.open('image/image.jpg')
img_array = np.array(img)

# Separate the image into R, G, B channels
r_channel = img_array[:, :, 0]
g_channel = img_array[:, :, 1]
b_channel = img_array[:, :, 2]

# Generate a Gaussian kernel
sigma = 3
gaussian_kernel = gaussian_kernel(size=30, sigma=sigma)

# Apply the filter to each color channel
r_filtered = apply_filter(r_channel, gaussian_kernel)
g_filtered = apply_filter(g_channel, gaussian_kernel)
b_filtered = apply_filter(b_channel, gaussian_kernel)

# Stack the filtered channels back into a color image
filtered_img_array = np.stack([r_filtered, g_filtered, b_filtered], axis=-1)

# Convert back to uint8 and save the result
filtered_img = Image.fromarray(np.clip(filtered_img_array, 0, 255).astype(np.uint8))
filtered_img.save('image/low_pass_image.jpg')
