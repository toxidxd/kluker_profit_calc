import cv2
import numpy as np

# Reading the main image
rgb_img = cv2.imread('image.jpg', 1)
# It is need to be convert it to grayscale
gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
# Reading the template image
template = cv2.imread('template_1.jpg', 0)
# Store width in variable w and height in variable h of template
w, h = template.shape[:-1]
# Now we perform match operations.
res = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
# Declare a threshold
threshold = 0.8
# Store the coordinates of matched location in a numpy array
loc = np.where(res >= threshold)
# Draw the rectangle around the matched region.
for pt in zip(*loc[::-1]):
    cv2.rectangle(rgb_img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
# Now display the final matched template image
# cv2.imshow('Detected', rgb_img)


