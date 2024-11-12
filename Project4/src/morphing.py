from PIL import Image
import numpy as np

# Load the two images
image_path1 = '../image/kohaku.png'
image_path2 = '../image/okita.png'
image1 = Image.open(image_path1).convert('RGB')  # Convert to RGB
image2 = Image.open(image_path2).convert('RGB')  # Convert to RGB

# Resize images to the same size if they are different
width = min(image1.width, image2.width)
height = min(image1.height, image2.height)
image1 = image1.resize((width, height))
image2 = image2.resize((width, height))

# Convert images to numpy arrays
array1 = np.array(image1, dtype=np.float32)
array2 = np.array(image2, dtype=np.float32)

# Function to perform linear interpolation and cross-dissolve between two images
def morph_images(array1, array2, alpha):
    # Linear interpolation and cross-dissolve using alpha
    morphed_array = (1 - alpha) * array1 + alpha * array2
    return np.clip(morphed_array, 0, 255).astype(np.uint8)

# Create a series of morphed images with different blending factors
for i, alpha in enumerate(np.linspace(0, 1, 11)):  # 11 steps from 0 to 1
    morphed_image_array = morph_images(array1, array2, alpha)
    morphed_image = Image.fromarray(morphed_image_array)
    output_path = f'../image/morph_sequence/morphed_image_{i}.jpg'
    morphed_image.save(output_path)
    print(f"Morphed image saved as '{output_path}' with alpha={alpha:.2f}")

print("Morphing process complete.")
