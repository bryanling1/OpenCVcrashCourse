import cv2
import numpy as np 

def empty(_):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("Trackbars", 640, 240)
cv2.createTrackbar("hue min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("hue max", "TrackBars", 105, 179, empty)
cv2.createTrackbar("sat min", "TrackBars", 139, 255, empty)
cv2.createTrackbar("sat max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("val min", "TrackBars", 134, 255, empty)
cv2.createTrackbar("val max", "TrackBars", 202, 255, empty)

img = cv2.imread("cards.jpg")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

while True: 
    h_min = cv2.getTrackbarPos("hue min", "TrackBars")
    h_max = cv2.getTrackbarPos("hue max", "TrackBars")
    s_min = cv2.getTrackbarPos("sat min", "TrackBars")
    s_max = cv2.getTrackbarPos("sat max", "TrackBars")
    v_min = cv2.getTrackbarPos("val min", "TrackBars")
    v_max = cv2.getTrackbarPos("val max", "TrackBars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(img_hsv, lower, upper)

    img_result = cv2.bitwise_and(img, img, mask=mask)

    # cv2.imshow("original", img)
    cv2.imshow("image", mask)

    # cv2.imshow("result", img_result)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break