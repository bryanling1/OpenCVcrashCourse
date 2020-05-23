import numpy as np 
import cv2

cards_img = cv2.imread("cards.jpg")

pts = np.float32([[228, 93], [429, 138], [159, 380], [367, 432]])
width, height = 250, 350
pts_location = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts, pts_location)
imgOutput = cv2.warpPerspective(cards_img, matrix, (width, height))

cv2.imshow("cards", imgOutput)

cv2.waitKey(0)

