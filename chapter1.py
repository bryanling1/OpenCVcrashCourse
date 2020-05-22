import cv2

#reading images
img = cv2.imread("image.jpg")

# cv2.imshow("window", img)
# cv2.waitKey(0)

#video
# cap = cv2.VideoCapture("outro.mp4")

# while True: 
#     success, img = cap.read()
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640) #width
cap.set(4, 480) #height
cap.set(10, -100) #brightness

while True: 
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
