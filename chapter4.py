import cv2
import numpy as np

img = np.random.uniform(0, 1, (500, 500, 3))
img[:] = (255, 0, 0)


#drawing lines
cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (0, 0, 0), 5)
cv2.rectangle(img, (0,0), (300, 300), (0, 0, 255), cv2.FILLED)
cv2.circle(img, (450, 450), 30, (0, 255, 0), 5)
cv2.putText(img, "LIGMA BALLS", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 150, 0), 3)

cv2.imshow("image", img)

cv2.waitKey(0)