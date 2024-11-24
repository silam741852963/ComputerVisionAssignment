# Import necessary packages
import numpy as np
import imutils
import cv2
import argparse
import os

class Stitcher:
    def __init__(self):
        pass

    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        # Unpack the images, detect keypoints, and extract descriptors
        (imageB, imageA) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)

        # Match features between the images
        M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)
        if M is None:
            return None, None  # Insufficient matches

        # Apply a perspective warp to stitch the images together
        (matches, H, status) = M
        result = cv2.warpPerspective(imageA, H,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        # If requested, create a visualization of keypoint matches
        vis = None
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status)
        return result, vis

    def detectAndDescribe(self, image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect and extract features using ORB
        descriptor = cv2.ORB_create()
        kps, features = descriptor.detectAndCompute(gray, None)

        # Convert keypoints to NumPy arrays
        kps = np.float32([kp.pt for kp in kps])
        return kps, features

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        # Match descriptors using Brute-Force matcher with Hamming distance
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(featuresA, featuresB)

        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)

        # Proceed if sufficient matches are found
        if len(matches) > 4:
            ptsA = np.float32([kpsA[m.queryIdx] for m in matches])
            ptsB = np.float32([kpsB[m.trainIdx] for m in matches])
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
            return matches, H, status
        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # Create an image to visualize matches
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB

        # Draw lines between matching keypoints
        for match in matches:
            ptA = (int(kpsA[match.queryIdx][0]), int(kpsA[match.queryIdx][1]))
            ptB = (int(kpsB[match.trainIdx][0]) + wA, int(kpsB[match.trainIdx][1]))
            cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
        return vis


def main():
    # Parse command-line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--first", required=True, help="Path to the first image")
    ap.add_argument("-s", "--second", required=True, help="Path to the second image")
    ap.add_argument("-o", "--output", required=True, help="Directory to save the output")
    args = vars(ap.parse_args())

    # Load and resize images for faster processing
    imageA = cv2.imread(args["first"])
    imageB = cv2.imread(args["second"])
    imageA = imutils.resize(imageA, height=400)
    imageB = imutils.resize(imageB, height=400)

    # Stitch images
    stitcher = Stitcher()
    (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

    if result is None:
        print("[ERROR] Image stitching failed. Not enough matches.")
        return

    # Save the results
    os.makedirs(args["output"], exist_ok=True)
    result_path = os.path.join(args["output"], "panorama.jpg")
    cv2.imwrite(result_path, result)
    print(f"[INFO] Panorama saved to {result_path}")

    if vis is not None:
        vis_path = os.path.join(args["output"], "matches.jpg")
        cv2.imwrite(vis_path, vis)
        print(f"[INFO] Matches visualization saved to {vis_path}")

    # Show results
    cv2.imshow("Image A", imageA)
    cv2.imshow("Image B", imageB)
    cv2.imshow("Keypoint Matches", vis)
    cv2.imshow("Panorama", result)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
