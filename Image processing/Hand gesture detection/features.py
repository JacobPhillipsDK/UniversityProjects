import cv2
import numpy as np
import math

# Function that calculates the farpoints
def convexity(maxContour):
    hull1 = cv2.convexHull(maxContour, returnPoints=False)
    defects = cv2.convexityDefects(maxContour, hull1)
    farPoints = []
    counter = 0

    try:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            far = tuple(maxContour[f][0])
            if d > 8000:
                counter += 1
                farPoints.append(far)
    except AttributeError:
        print(AttributeError)
    return len(farPoints)

def ColorToGray(input):
    outputGray = np.zeros((input.shape[0],input.shape[1]),np.uint8)
    for y, row in enumerate(input):
        for x, v in enumerate(row):
            outputGray[y, x] = round(v[0] * 0.299 + v[1] * 0.587 + v[2] * 0.114)
    return outputGray

# Function for finding the bounding box of the hand.
# It takes in 3 arguments, a threshold image, xDistance and yDistance
# xDistance and yDistance is already defined as bigX-smallX and bigY-smallY
def boundingbox(threshold,xDistance,yDistance):
    whitePixel = 0
    ratio = 0
    for y in range(yDistance):
        for x in range(xDistance):
            if threshold[y][x] == 255:
                whitePixel += 1
    allpix = xDistance * yDistance
    blackpix = allpix - whitePixel
    try:
        ratio = blackpix / whitePixel
    except ZeroDivisionError:
        print("Attempted to divide something with zero in bounding box:",ZeroDivisionError)
    return whitePixel, blackpix, ratio

# Function that calculates the circularity on and object.
# Takes in the contours of an object as its only argument.

def calculatePeriCirc(contour):
    perimeter = cv2.arcLength(contour, True)
    try:
        circularity = 4 * math.pi * cv2.contourArea(contour) / pow(perimeter, 2)
    except ZeroDivisionError:
        circularity = 0
        print("System Message: Did not calculate PeriCirc due to:",ZeroDivisionError)
    return float(perimeter), float(circularity)

# Function that counts the amount of white pixels
# on both the left and right side.
# Takes in a thresholded image and the centerX variable
# as arguments.

def calcPixelsLeftRight(image, centerX):
    imageLcount, imageRcount, ratio = 0,0,0
    drawingLR = np.zeros((image.shape[0], image.shape[1],3), np.uint8)

    for y in range (0, image.shape[0]-1):
        for x in range (0, centerX):
            if image[y][x] == 255:
                imageLcount += 1
                drawingLR[y][x] = (255,0,0)

    for y in range (0, image.shape[0]):
        for x in range (centerX,image.shape[1]-1):
            if image[y][x] == 255:
                imageRcount += 1
                drawingLR[y][x] = (0,255,0)

    try:
        ratio = imageLcount/imageRcount
    except ZeroDivisionError:
        print(ZeroDivisionError)

    cv2.imshow("drawing",drawingLR)

    return imageLcount, imageRcount, ratio

# Function that calculates the center of the hand.
# It takes in the convexhull of the hand as its only argument.

def calculateCenter(convexInput):
    centerHandY, centerHandX = 100,100
    smallX, bigX, smallY, bigY, bigYX, bigXY, smallYX, smallXY = 0,0,0,0,0,0,0,0
    if (len(convexInput)) > 1:
        for b in range (len(convexInput)):
            dataHoldY = convexInput[b][0][0] # for at finde Y
            dataHoldX = convexInput[b][0][1] # for at finde X
            if smallY == 0:
                smallX, bigX, smallY, bigY = dataHoldX, dataHoldX, dataHoldY, dataHoldY
                bigYX, bigXY, smallYX, smallXY = dataHoldX,dataHoldY, dataHoldX, dataHoldY
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

        # ("SmallX:",smallX,smallXY,"BigX:",bigX,bigXY,"SmallY:",smallY,smallYX,"BigY:",bigY,bigYX)
        centerHandY, centerHandX = (bigY+smallY)/2, (bigX+smallX)/2

    return int(centerHandY), int(centerHandX), int(smallX), int(bigX), int(smallY), int(bigY), int(smallXY), int(bigXY), int(smallYX), int(bigYX)
