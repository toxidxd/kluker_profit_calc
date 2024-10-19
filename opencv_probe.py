import cv2
import numpy as np
# Reading the main image
img_rgb = cv2.imread(r'screenshots/img_low_5.jpg',1)
# It is need to be convert it to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# Read the template
template = cv2.imread(r'templates/5.jpg',0)
# Store width in variable w and height in variable h of template
print(template.shape)
w, h = template.shape
# Now we perform match operations.
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
# Declare a threshold
threshold = 0.8
# Store the coordinates of matched region in a numpy array
loc = np.where( res >= threshold)
print(loc)
# Draw a rectangle around the matched region.
for pt in zip(*loc[::-1]):
 print(pt)
 print(pt[0] + w, pt[1] + h)
 cv2.rectangle(img_rgb, pt,(pt[0] + w, pt[1] + h),(0,255,255), 2)
# Now display the final matched template image
# cv2.imshow('Detected',img_rgb)
# input()
cv2.imwrite('cvtest.jpg', img_rgb)