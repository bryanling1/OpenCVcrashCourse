import cv2
import numpy as np 

faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 10)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break