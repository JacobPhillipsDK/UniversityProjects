import numpy as np
import cv2
import math

# define a video capture object
cap = cv2.VideoCapture(0)

# Reading the video file until finished
frameCount = 0
frameCount = frameCount + 1
_, bg, = cap.read()
hit = np.array([[255, 255, 255],
                [255, 255, 255],
                [255, 255, 255]])


def erotion(threshold):
    newArray = np.zeros((threshold.shape[0], threshold.shape[1], 3), np.uint8)
    for y in range(threshold.shape[0]):
        for x in range(threshold.shape[1]):
            crop = threshold[y:y + 3, x:x + 3]
            croparray = np.array(crop)
            if np.all(hit == croparray) and x > 1 and y > convex and x < threshold.shape[1] - 1 and y < threshold.shape[
                0] - 1:
                newArray[y][x] = 255
            elif y <= convex:
                newArray[y][x] = threshold[y][x]
    return newArray


def dilation(threshold):
    newArray = np.zeros((threshold.shape[0], threshold.shape[1], 3), np.uint8)
    for y in range(threshold.shape[0]):
        for x in range(threshold.shape[1]):
            crop = threshold[y:y + 3, x:x + 3]
            croparray = np.array(crop)
            if np.any(hit == croparray) and x > 1 and y > convex and x < threshold.shape[1] - 1 and y < threshold.shape[
                0] - 1:
                newArray[y][x] = 255
                newArray[y][x + 1] = 255
                newArray[y + 1][x + 1] = 255
                newArray[y + 1][x] = 255
                newArray[y - 1][x] = 255
                newArray[y][x - 1] = 255
                newArray[y - 1][x - 1] = 255
            elif x > 1 and y > 1 and x < threshold.shape[1] - 1 and y < threshold.shape[0] - 1:
                newArray[y][x] = threshold[y][x]
    return newArray


def convexity(maxContour):
    hull1 = cv2.convexHull(maxContour, returnPoints=False)
    defects = cv2.convexityDefects(maxContour, hull1)
    farPoints = []
    counter = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        far = tuple(maxContour[f][0])
        start = tuple(maxContour[s][0])
        end = tuple(maxContour[e][0])
        # print("start:",start,"end:",end)
        # cv2.line(drawing, start, end, [0, 255, 0], 2)
        if d > 10000 and start[1] < 100 and end[1] < 100:
            counter += 1
            farPoints.append(far)
            print("finger", str(counter), ":", start)
            cv2.circle(drawing, far, 5, [0, 255, 0], -1)
            cv2.circle(drawing, start, 5, [255, 0, 0], -1)
            cv2.circle(drawing, end, 5, [255, 0, 0], -1)
            print("finger 2:", end)
            print("far:", far[1])
    return farPoints[0][1]


def boundingbox(threshold, xDistance, yDistance):
    whitePixel = 0
    for y in range(yDistance):
        for x in range(xDistance):
            if threshold[y][x] == 255:
                whitePixel += 1
    allpix = xDistance * yDistance
    blackpix = allpix - whitePixel
    ratio = blackpix / whitePixel
    return whitePixel, blackpix, ratio


def calculatePeriCirc(contour):
    perimeter = cv2.arcLength(contour, True)
    circularity = 4 * math.pi * cv2.contourArea(contour) / pow(perimeter, 2)
    print("PERIMETER:", perimeter, "Circularity:", circularity)
    return float(perimeter), float(circularity)


def calcPixelsLeftRight(image, centerX):
    print("GOTCENTER:", centerX)
    imageLcount, imageRcount = 0, 0
    drawingLR = np.zeros((200, 200, 3), np.uint8)

    for y in range(0, 200):
        for x in range(0, centerX):
            if image[y][x] == 255:
                imageLcount += 1
                drawingLR[y][x] = (255, 0, 0)

    for y in range(0, 200):
        for x in range(centerX, 200):
            if image[y][x] == 255:
                imageRcount += 1
                drawingLR[y][x] = (0, 255, 0)

    cv2.imshow("drawing", drawingLR)
    print("CenterHand", centerHandX, "Pixels Left:", imageLcount, "Pixels Right:", imageRcount)

    return imageLcount, imageRcount


def calculateAngles(y, x, centerY, centerX):
    radian = math.atan2((y - centerY), (x - centerX))
    degrees = math.degrees(radian)
    return degrees


def pythagoras(points):
    hold = ((points[0] * points[0]) + (points[1] * points[1]))
    length = math.sqrt(hold)
    return length


def newCalculateLength(centerHandY, centerHandX, smallX, smallXY, smallY, smallYX, bigX, bigXY, bigY, bigYX):
    lengthSmallX = (smallXY - centerHandY, smallX - centerHandX)
    lengthBigX = (bigXY - centerHandY, bigX - centerHandX)
    lengthSmallY = (smallY - centerHandY, smallYX - centerHandX)
    lengthBigY = (bigY - centerHandY, bigYX - centerHandX)

    print("Length:", lengthSmallX, lengthBigX, lengthSmallY, lengthBigY)

    lengthSmallX = pythagoras(lengthSmallX)
    lengthBigX = pythagoras(lengthBigX)
    lengthSmallY = pythagoras(lengthSmallY)
    lengthBigY = pythagoras(lengthBigY)

    print("Pythagoras: SmallY", lengthSmallX, "BigY", lengthBigX, "SmallX", lengthSmallY, "BigX", lengthBigY)

    return lengthSmallX, lengthBigX, lengthSmallY, lengthBigY


def calculateCenter(convexInput):
    centerHandY, centerHandX = 100, 100

    smallX, bigX, smallY, bigY, bigYX, bigXY, smallYX, smallXY = 0, 0, 0, 0, 0, 0, 0, 0
    if (len(convexInput)) > 1:
        for b in range(len(convexInput)):
            dataHoldY = convexInput[b][0][0]  # for at finde Y
            dataHoldX = convexInput[b][0][1]  # for at finde X

            if smallY == 0:
                smallX, bigX, smallY, bigY = dataHoldX, dataHoldX, dataHoldY, dataHoldY
                bigYX, bigXY, smallYX, smallXY = dataHoldX, dataHoldY, dataHoldX, dataHoldY
            if dataHoldY > bigY:
                bigY = dataHoldY
                bigYX = dataHoldX
            if dataHoldY < smallY:
                smallY = dataHoldY
                smallYX = dataHoldX
            if dataHoldX > bigX:
                bigX = dataHoldX
                bigXY = dataHoldY
            if dataHoldX < smallX:
                smallX = dataHoldX
                smallXY = dataHoldY

        print("SmallX:", smallX, smallXY, "BigX:", bigX, bigXY, "SmallY:", smallY, smallYX, "BigY:", bigY, bigYX)
        centerHandY, centerHandX = (bigY + smallY) / 2, (bigX + smallX) / 2

    return int(centerHandY), int(centerHandX), int(smallX), int(bigX), int(smallY), int(bigY), int(smallXY), int(
        bigXY), int(smallYX), int(bigYX)


while True:
    ret, frame = cap.read()
    frameCount += 1

    # if video finished or no Video Input
    if not ret:
        break

    # displaying the frame with fps
    grayFrameHSV = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    feedHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(grayFrameHSV, feedHSV)
    diff = diff[100:300, 100:300]

    cv2.imshow("frame2", diff)
    # https://www.learnopencv.com/convex-hull-using-opencv-in-python-and-c/

    hull = []

    if cv2.waitKey(1) & 0xFF == ord('e'):
        blur = cv2.blur(diff, (5, 5))  # blur the image
        threshold = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow("thresh", threshold)
        (contours, hierachy) = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros((threshold.shape[0], threshold.shape[1], 3), np.uint8)
        drawingResize = drawing[100:300, 100:300]

        # Line drawing: https://stackoverflow.com/questions/39785476/draw-line-on-webcam-stream-python

        for i in range(len(contours)):
            color_contours = (0, 0, 255)
            color = (255, 0, 0)
            cv2.drawContours(drawing, contours, i, color_contours, 1, 8)
            if len(contours) > 0:
                maxContour = max(contours, key=cv2.contourArea)

        for i in range(2):
            hull.append(cv2.convexHull(maxContour))
            cv2.drawContours(drawing, hull, i, color, 1, 8)
            normArray = np.array(hull, dtype=object)

            centerHandY, centerHandX, smallX, bigX, smallY, bigY, smallXY, bigXY, smallYX, bigYX = calculateCenter(
                normArray[i])
            exLeftAngle = calculateAngles(smallXY, smallX, centerHandY, centerHandX)
            exRightAngle = calculateAngles(bigXY, bigX, centerHandY, centerHandX)
            exTopAngle = calculateAngles(smallY, smallYX, centerHandY, centerHandX)
            exBotAngle = calculateAngles(bigY, bigYX, centerHandY, centerHandX)

            calcPixelsLeftRight(threshold, centerHandY)

            # print("EXTREME LEFT:", calculateAngles(smallXY, smallX, centerHandY, centerHandX))
            # print("EXTREME RIGHT:", calculateAngles(bigXY, bigX, centerHandY, centerHandX))
            # print("EXTREME TOP:", calculateAngles(smallY, smallYX, centerHandY, centerHandX))
            # print("EXTREME BOTTOM:", calculateAngles(bigY, bigYX, centerHandY, centerHandX))
            calculatePeriCirc(maxContour)

            yDist = bigY - smallY
            xDist = bigX - smallX

            drawing2 = np.zeros((xDist, yDist, 3), np.uint8)
            thresholdResize = threshold[smallX:bigX, smallY:bigY]
            array = np.array(thresholdResize)
            whitePixel, blackpix, ratio = boundingbox(array, yDist, xDist)
            print("Ratio:", ratio)
            print("whitepixels: ", whitePixel)
            print("height: ", yDist)
            print("width: ", xDist)

            cv2.line(drawing, pt1=(smallXY, smallX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)
            cv2.line(drawing, pt1=(bigXY, bigX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)
            cv2.line(drawing, pt1=(smallY, smallYX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)
            cv2.line(drawing, pt1=(bigY, bigYX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)

            if len(hull) > 1:
                lengthSmallX, lengthBigX, lengthSmallY, lengthBigY = newCalculateLength(centerHandY, centerHandX,
                                                                                        smallX, smallXY, smallY,
                                                                                        smallYX, bigX, bigXY, bigY,
                                                                                        bigYX)
                print("CONVEXHULL: ", i)
            try:
                convex = convexity(maxContour)
            except ZeroDivisionError:
                ratio = 0
            dialate = dilation(threshold)
            dialate2 = dilation(dialate)
            erode = erotion(dialate2)
            erode2 = erotion(erode)
            graylort = cv2.cvtColor(erode2, cv2.COLOR_BGR2GRAY)
            thresholderode = cv2.threshold(graylort, 30, 255, cv2.THRESH_BINARY)[1]
            (contours1, _) = cv2.findContours(thresholderode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            drawing2 = np.zeros((erode2.shape[0], erode2.shape[1], 3), np.uint8)
            for i in range(len(contours1)):
                cv2.drawContours(drawing2, contours1, i, color_contours, 1, 8)
                if len(contours1) > 0:
                    maxContour1 = max(contours1, key=cv2.contourArea)
            for i in range(2):
                hull.append(cv2.convexHull(maxContour1))
                cv2.drawContours(drawing2, hull, i, color, 1, 8)
        cv2.imshow("Convex", drawing)
        cv2.imshow("dialate", dialate2)
        cv2.imshow("erotion", erode2)
        cv2.imshow("newconvex", drawing2)

    # press 'Q' if you want to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        _, bg = cap.read()

# When everything done, release the capture
cap.release()
# Destroy all the windows now
cv2.destroyAllWindow()
