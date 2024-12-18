import cv2
import numpy as np


def get_borders(img, template):
    # Reading the main image
    rgb_img = cv2.imread(img, 1)
    w_img = rgb_img.shape[1]
    # It is need to be convert it to grayscale
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    # Reading the template image
    template = cv2.imread(template, 0)
    # Store width in variable w and height in variable h of template
    w, h = template.shape
    # Now we perform match operations.
    res = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    # Declare a threshold
    threshold = 0.8
    # Store the coordinates of matched location in a numpy array
    loc = np.where(res >= threshold)

    if len(loc[0]) != 0:

        result = (0, int(loc[0][0]), w_img, int(loc[0][0] + h))
        return result

    else:
        return 0
