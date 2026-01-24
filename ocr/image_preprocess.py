import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )

    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    return cleaned
