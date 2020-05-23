import cv2
import numpy as np 

def getContours(img, draw):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        cv2.drawContours(draw, cnt, -1, (0, 255 ,0), 2)
        
        #sometimes check with if statement here
        arc_len = cv2.arcLength(cnt, True)
        points = cv2.approxPolyDP(cnt, 0.01*arc_len, True)
        len_points = len(points)
        x, y, w, h = cv2.boundingRect(points)

        objType = ""
        if len_points == 3: objType = "Triangle"
        elif len_points == 4: 
            ratio = w / float(h)
            if ratio > 0.95 or ratio < 1.05:
                objType = "Square"
            else:
                objType = "rectangle"
        elif len_points > 4:
            objType = "circle"
    
        cv2.rectangle(draw, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(draw, objType, (x, y + 10), cv2.FONT_HERSHEY_PLAIN, 1, 4)
        
    
   

img = cv2.imread("shapes.png")

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (7, 7), 1)
img_canny = cv2.Canny(img_blur, 150, 150)

getContours(img_canny, img)

cv2.imshow("image", img)
cv2.waitKey(0)