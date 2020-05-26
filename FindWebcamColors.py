import numpy as np 
import cv2
import pdb

def empty(_):
    pass

def findWebcamColors():
    cm = cv2.VideoCapture(0)
    cm.set(3, 500)
    cm.set(4, 300)

    cv2.namedWindow("track")
    cv2.resizeWindow("track", 500, 300)
    cv2.createTrackbar("hue min", "track", 0, 179, empty)
    cv2.createTrackbar("hue max", "track", 179, 179, empty)
    cv2.createTrackbar("sat min", "track", 0, 255, empty)
    cv2.createTrackbar("sat max", "track", 255, 255, empty)
    cv2.createTrackbar("val min", "track", 0, 255, empty)
    cv2.createTrackbar("val max", "track", 255, 255, empty)

    while True:
        success, img = cm.read()
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("hue min", "track")
        h_max = cv2.getTrackbarPos("hue max", "track")
        s_min = cv2.getTrackbarPos("sat min", "track")
        s_max = cv2.getTrackbarPos("sat max", "track")
        v_min = cv2.getTrackbarPos("val min", "track")
        v_max = cv2.getTrackbarPos("val max", "track")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(img_hsv, lower, upper)
        mask_temp = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        img_with_mask = cv2.bitwise_and(img, img, mask=mask)

        stack = np.hstack((img, mask_temp))
        cv2.imshow("Camera", stack)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

findWebcamColors()

