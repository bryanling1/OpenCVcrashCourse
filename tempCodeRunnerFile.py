     cv2.drawContours(draw, cnt, -1, (0, 255 ,0), 2)
            arc_len = cv2.arcLength(cnt, True)
            points = cv2.approxPolyDP(cnt, 0.01*arc_len, True)
            x, y, w, h = cv2.boundingRect(points)