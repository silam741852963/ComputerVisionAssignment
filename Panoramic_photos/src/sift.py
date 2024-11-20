import cv2
import numpy as np
import os
import time
import matplotlib.pyplot as plt

# Create output folder if it doesn't exist
os.makedirs('../output', exist_ok=True)

def read_images(folder_path):
    """Read images from a folder."""
    images = []
    for i in range(1, 4):
        image_path = os.path.join(folder_path, f"example_{i}.jpg")
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image {image_path} not found.")
        images.append(image)
    return images

def stitch_images_sift(images):
    """Stitch images using SIFT and OpenCV's Stitcher."""
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    (status, panorama) = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        return panorama
    else:
        raise Exception(f"Stitching failed with status code {status}")

# def stitch_images_orb(images):
#     """Stitch images manually using ORB and homography."""
#     orb = cv2.ORB_create()
#     matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

#     # Use the first image as the base for stitching
#     panorama = images[0]

#     for i in range(1, len(images)):
#         # Detect and compute ORB keypoints and descriptors
#         kp1, des1 = orb.detectAndCompute(panorama, None)
#         kp2, des2 = orb.detectAndCompute(images[i], None)

#         # Match descriptors
#         matches = matcher.match(des1, des2)
#         matches = sorted(matches, key=lambda x: x.distance)

#         # Extract matched points
#         src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
#         dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

#         # Compute the homography matrix
#         H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

#         # Warp the panorama image to align with the current image
#         height, width = images[i].shape[:2]
#         panorama = cv2.warpPerspective(panorama, H, (panorama.shape[1] + width, max(panorama.shape[0], height)))

#         # Overlay the current image onto the panorama
#         panorama[0:height, 0:width] = images[i]

#     return panorama

def save_and_display_image(image, output_path, title):
    """Save and display an image."""
    cv2.imwrite(output_path, image)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

def main():
    # Read images from the folder
    folder_path = "../image"
    images = read_images(folder_path)

    # SIFT Panorama
    try:
        start_time = time.time()
        panorama_sift = stitch_images_sift(images)
        end_time = time.time()
        print(f"SIFT Stitching completed in {end_time - start_time:.2f} seconds.")
        sift_output_path = "../output/panorama_sift.jpg"
        save_and_display_image(panorama_sift, sift_output_path, "Panorama using SIFT")
    except Exception as e:
        print(f"SIFT Stitching failed: {e}")

    # # ORB Panorama
    # try:
    #     start_time = time.time()
    #     panorama_orb = stitch_images_orb(images)
    #     end_time = time.time()
    #     print(f"ORB Stitching completed in {end_time - start_time:.2f} seconds.")
    #     orb_output_path = "../output/panorama_orb.jpg"
    #     save_and_display_image(panorama_orb, orb_output_path, "Panorama using ORB")
    # except Exception as e:
    #     print(f"ORB Stitching failed: {e}")

if __name__ == "__main__":
    main()
