from PIL import Image, ImageEnhance

# Load the image
image_path = '../image/teapot.jpg'
image = Image.open(image_path)

# Function to apply an image filter by changing the contrast
def adjust_contrast(image, factor, output_path):
    enhancer = ImageEnhance.Contrast(image)
    filtered_image = enhancer.enhance(factor)
    filtered_image.save(output_path)
    return filtered_image

# Apply contrast adjustment with different factors and save images
low_contrast = adjust_contrast(image, 0.5, '../image/low_contrast_image.jpg')   # Reduced contrast
high_contrast = adjust_contrast(image, 2.0, '../image/high_contrast_image.jpg')  # Increased contrast

print("Filtered images saved as 'low_contrast_image.jpg' and 'high_contrast_image.jpg'")
