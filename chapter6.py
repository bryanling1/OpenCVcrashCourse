import cv2
import numpy as np

img = cv2.imread("cards.jpg")

hor = np.vstack((img, img))

cv2.imshow("stack", hor)

cv2.waitKey(0)