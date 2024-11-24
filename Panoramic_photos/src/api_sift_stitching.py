import cv2
import numpy as np
import argparse
import os

def load_images(image_dir, image_prefix):
    images = []
    for filename in sorted(os.listdir(image_dir)):
        if filename.startswith(image_prefix):
            image_path = os.path.join(image_dir, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image {image_path}")
                continue
            images.append(image)
    return images

def stitch_images(images):
    if len(images) < 2:
        print("Need at least two images to stitch.")
        return None

    # Create a Stitcher object
    stitcher = cv2.Stitcher_create()
    stitcher.setPanoConfidenceThresh(0.5)
    stitcher.setWaveCorrection(True)

    # Perform stitching
    status, stitched_image = stitcher.stitch(images)
    if status != cv2.Stitcher_OK:
        print(f"Image stitching failed with status code {status}.")
        return None
    return stitched_image

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_dir", type=str, required=True, help="Path to the input images directory")
    ap.add_argument("-o", "--output", type=str, required=True, help="Path to the output image")
    ap.add_argument("-p", "--prefix", type=str, default='image_', help="Input image filename prefix")
    args = vars(ap.parse_args())

    images = load_images(args["input_dir"], args["prefix"])
    if len(images) < 2:
        print("Need at least two images to stitch.")
        return

    result = stitch_images(images)
    if result is None:
        print("Image stitching failed.")
        return

    cv2.imwrite(args["output"], result)
    print(f"Stitched image saved as {args['output']}")

if __name__ == "__main__":
    main()
