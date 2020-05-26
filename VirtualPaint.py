import numpy as np 
import cv2 
import keyboard

cap = cv2.VideoCapture(0)
cap.set(3, 500) #width
cap.set(4, 400) #height
# cap.set(10, -100) #brightness

myColors = [[106, 198, 0, 157, 255, 255]]
myColorValues = [(185, 128, 41)]
pointsToDraw = [] #(x, y, colorId)

def drawPoints(pointsToDraw, img, radius):
    for point in pointsToDraw:
        center = (point[0], point[1])
        color = myColorValues[point[2]]
        cv2.circle(img, center, radius, color, cv2.FILLED)

def findColor(img, colors):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(img_hsv, lower, upper)
        x, y = getContours(mask, img)
        if(x != -1 and y != -1):
            pointsToDraw.append((x, y, count))
        cv2.circle(img, (x, y), 10, myColorValues[count], cv2.FILLED)
        count += 1

def getContours(img, draw):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h, = -1, -1, -1, -1
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 240:
            cv2.drawContours(draw, cnt, -1, (0, 255 ,0), 2)
            arc_len = cv2.arcLength(cnt, True)
            points = cv2.approxPolyDP(cnt, 0.01*arc_len, True)
            x, y, w, h = cv2.boundingRect(points)
    
    return x+w//2, y



is_on = True

while True: 
    success, img = cap.read()
    findColor(img, myColors)
    drawPoints(pointsToDraw, img, 10)
    img_flipped = cv2.flip(img, 1) 
    cv2.imshow("Video", img_flipped)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
