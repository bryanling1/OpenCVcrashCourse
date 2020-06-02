import numpy as np
import cv2
from PIL import Image
from mss import mss
import pdb
import skimage.measure
import time

def empty(_):
    pass

def createMask(img, limits, invert=False):
    """
    Creates a Gray scale mask with hsv given upper and lower limit ranges

    img: BRG Image
    """
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, limits[0], limits[1])
    if invert == True:
        mask = np.invert(mask)
    return mask

def getMaskArea(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    area = 0
    for contour in contours:
        area += cv2.contourArea(contour)
    return area

def maxpool(img, f):
    img = skimage.measure.block_reduce(img, (f, f, 1), np.max)
    return img

def bc(img, b, c):
    a = c
    return cv2.addWeighted(img, a, np.zeros(img.shape, img.dtype), 0, b)

def layerHSVMasks(img, limits, subtract=False):
    """
    Cleans the map by using HSV masks to remove certain objects

    Removes the background environment and roads
    """
    masks = []
    for limit in limits:
       masks.append(createMask(img, limit, subtract))

    #init the first one
    output = cv2.bitwise_and(img, img, mask=masks[0])
    for i in range(1, len(masks)):
        output = cv2.bitwise_and(output, output, mask=masks[i])
    return output

def findScreenColors(top, left, width, height, b, c, pool, display_width, display_height):
    mon = {'top': top,'left': left, 'width': width, 'height': height}
    sct = mss()

    cv2.namedWindow("track")
    cv2.resizeWindow("track", 500, 300)
    cv2.createTrackbar("hue min", "track", 0, 179, empty)
    cv2.createTrackbar("hue max", "track", 179, 179, empty)
    cv2.createTrackbar("sat min", "track", 0, 255, empty)
    cv2.createTrackbar("sat max", "track", 255, 255, empty)
    cv2.createTrackbar("val min", "track", 0, 255, empty)
    cv2.createTrackbar("val max", "track", 255, 255, empty)
    current_area = 0

    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    img = np.array(img)
    img = maxpool(img, pool)
    img = bc(img, b, c)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    while True:
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
        out_img = np.hstack([img, mask_temp])

        area = getMaskArea(mask)
        if area != current_area:
            current_area = area
            print(current_area/(img.shape[0] * img.shape[1]))

        # out_img = cv2.resize(out_img, (display_width, display_height), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('test', out_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    # time.sleep(0.5)

def findScreenColorsN(top, left, width, height, b, c, pool, display_width, display_height, n=1):
    mon = {'top': top,'left': left, 'width': width, 'height': height}
    sct = mss()
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    img = np.array(img)
    img = maxpool(img, pool)
    img = bc(img, b, c)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i in range(n):
        cv2.namedWindow("track"+str(i))
        cv2.resizeWindow("track"+str(i), 500, 300)
        cv2.createTrackbar("hue min", "track"+str(i), 0, 179, empty)
        cv2.createTrackbar("hue max", "track"+str(i), 179, 179, empty)
        cv2.createTrackbar("sat min", "track"+str(i), 0, 255, empty)
        cv2.createTrackbar("sat max", "track"+str(i), 255, 255, empty)
        cv2.createTrackbar("val min", "track"+str(i), 0, 255, empty)
        cv2.createTrackbar("val max", "track"+str(i), 255, 255, empty)
    
    #init variables
    data = {}
    for i in range(n):
        data["h_min"+str(i)] = 0
        data["h_max"+str(i)] = 0
        data["s_min"+str(i)] = 0
        data["s_max"+str(i)] = 0
        data["v_min"+str(i)] = 0
        data["v_max"+str(i)] = 0

    while True:
        masks = []
        limits = []
        for i in range(n):
            data["h_min"+str(i)] =  cv2.getTrackbarPos("hue min", "track"+str(i))
            data["h_max"+str(i)] =  cv2.getTrackbarPos("hue max", "track"+str(i))
            data["s_min"+str(i)] =  cv2.getTrackbarPos("sat min", "track"+str(i))
            data["s_max"+str(i)] =  cv2.getTrackbarPos("sat max", "track"+str(i))
            data["v_min"+str(i)] =  cv2.getTrackbarPos("val min", "track"+str(i))
            data["v_max"+str(i)] =  cv2.getTrackbarPos("val max", "track"+str(i))
            h_min = data["h_min"+str(i)]
            h_max = data["h_max"+str(i)]
            s_min = data["s_min"+str(i)]
            s_max = data["s_max"+str(i)]
            v_min = data["v_min"+str(i)]
            v_max = data["v_max"+str(i)]
            limits.append([(h_min, s_min, v_min), (h_max, s_max, v_max)])
            lower = np.array([data["h_min"+str(i)], data["s_min"+str(i)], data["v_min"+str(i)]])
            upper = np.array([data["h_max"+str(i)], data["s_max"+str(i)], data["v_max"+str(i)]])
            mask = cv2.inRange(img_hsv, lower, upper)
            mask_temp = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            out_img = mask
            masks.append(out_img)

            # out_img = cv2.resize(out_img, (display_width, display_height), interpolation=cv2.INTER_LINEAR)
            cv2.imshow('test'+str(i), out_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        final_image = layerHSVMasks(img, limits, True)
        cv2.imshow('final', final_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        cv2.imshow('original', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        

findScreenColorsN(0, 0, 3000, 2000, -70, 1.3, 4, 1000*2, 666, 6)