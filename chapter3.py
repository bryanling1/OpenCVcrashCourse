import cv2

img = cv2.imread("./image.jpg")
imgResize = cv2.resize(img, (500, 600))
imgCropped = imgResize[0:200, 200:500]

cv2.imshow("Image", imgCropped)

cv2.waitKey(0)