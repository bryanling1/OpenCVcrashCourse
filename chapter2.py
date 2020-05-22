import cv2
import numpy as np

img = cv2.imread("image.jpg")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (101, 101), 0) #kernel has to be odd numbers
imgCanny = cv2.Canny(img, 0, 50) #detect outlines

kernel = np.ones((2, 2), np.uint8)
imgDialation = cv2.dilate(imgCanny, kernel, iterations=5)

imgEroded = cv2.erode(imgDialation, kernel, iterations=1)

cv2.imshow("Eroded", imgEroded)
cv2.waitKey(0)