import numpy as np
import cv2
import math
import os
import features

windowsOS = True

try:
    import musicControl
except ModuleNotFoundError: windowsOS = False


# define a video capture object
cap = cv2.VideoCapture(0)

# Reading the video file until finished
frameCount = 0
frameCount = frameCount+1
_, bg, = cap.read()

# Function we use to load our templatedata
def loadTemplateData():
    templateData = []

    print("getCwd",os.getcwd())
    templateData.append(np.genfromtxt("Template-image/dataset_pause.txt", dtype="float"))
    templateData.append(np.genfromtxt("Template-image/dataset_volumeup.txt", dtype="float"))
    templateData.append(np.genfromtxt("Template-image/dataset_volumedown.txt", dtype="float"))
    templateData.append(np.genfromtxt("Template-image/dataset_songnext.txt", dtype="float"))
    templateData.append(np.genfromtxt("Template-image/dataset_songprevious.txt", dtype="float"))

    templateData = np.array(templateData)
    templateData = templateData.tolist()
    print("ToList",templateData)
    for i in range (len(templateData)):
        print("HandGesture:",i,templateData[i])
        for z in range (len(templateData[i])):
            print("HandGesture:",i,"dataNumber",z,templateData[i][z])

    return templateData

# The function which compares the different features
# and then decides which hand gesture is in the frame
def newCompareInputTemplate(inputData):
    mostAccurate = [[100]]
    templateData = loadTemplateData()
    weightLRscale, weightFarPoints, weightBounding, weightCircularity = 2,8,3,1
    sumWeight = (weightLRscale+weightFarPoints+weightBounding+weightCircularity)

    for i in range(len(templateData)):
        for t in range(len(templateData[i])):
            dataHold = []
            for r in range (4):
                if templateData[i][t][r] == 0 or inputData[r] == 0:
                    print("[DATA:",i,t,r,"]","Ratio number:",r,"dividing",templateData[i][t][r],"with",inputData[r])
                    if templateData[i][t][r] == 0 and inputData[r] == 0:
                        dataHold.append(1)
                    else:
                        dataHold.append(0)
                else:
                        ratio = templateData[i][t][r] / inputData[r]
                        dataHold.append(ratio)
                        print("[DATA:",i,t,r,"]","Ratio number:",r,"dividing",templateData[i][t][r],"with",inputData[r],"ratio",ratio)

            averageAllFeatures = ((dataHold[0]*weightLRscale)+(dataHold[1]*weightFarPoints)+(dataHold[2]*weightBounding)+(dataHold[3]*weightCircularity))/sumWeight

            averageAllFeaturesToOne = averageAllFeatures-1
            if averageAllFeaturesToOne < 0:
                averageAllFeaturesToOne = ((averageAllFeaturesToOne-1)*-1)

            if averageAllFeaturesToOne<mostAccurate[0][0]:
                mostAccurate[0] = (averageAllFeaturesToOne, str(i), str(t), str(r))
                print("UpdatedMostAccurate", averageAllFeaturesToOne, i, t, r)
                print(i, t, r, "printing individual data:", templateData[i][t][r])
        print("Finished searching in folder",i)
    print("Finished Comparing...:",mostAccurate)

    try:
        if int(mostAccurate[0][1]) == 0:
            print("Hand gesture found: Stop/start")
            if windowsOS: musicControl.musicControl.play(None)
        if int(mostAccurate[0][1]) == 1:
            print("Hand gesture found: Volume up")
            if windowsOS: musicControl.musicControl.volup(None)
        if int(mostAccurate[0][1]) == 2:
            print("Hand gesture found: Volume down")
            if windowsOS: musicControl.musicControl.voldown(None)
        if int(mostAccurate[0][1]) == 3:
            print("Hand gesture found: Song next")
            if windowsOS: musicControl.musicControl.next(None)
        if int(mostAccurate[0][1]) == 4:
            print("Hand gesture found: Song previous")
            if windowsOS: musicControl.musicControl.prev(None)
    except IndexError: print("No data to compare")


while True:
    ret, frame = cap.read()
    frameCount += 1

    # if video finished or no Video Input
    if not ret:
        break

    # displaying the frame with fps
    grayFrameHSV = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    feedHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(grayFrameHSV,feedHSV)
    diff = diff[100:300, 100:300]

    cv2.imshow("frame2", diff)
    # https://www.learnopencv.com/convex-hull-using-opencv-in-python-and-c/

    hull = []
    # The code that runs when the user pushes the e button.
    # This is where we call most of our functions.
    if cv2.waitKey(1) & 0xFF == ord('e'):
        blur = cv2.blur(diff, (5, 5))  # blur the image
        threshold = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY)[1] #threshold the image
        cv2.imshow("thresh",threshold)
        (im2, contours, hierachy) = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Finding contours
        drawing = np.zeros((threshold.shape[0], threshold.shape[1], 3), np.uint8)
        drawingResize = drawing[100:300,100:300]

        # Line drawing: https://stackoverflow.com/questions/39785476/draw-line-on-webcam-stream-python
        # Drawing the contours
        for i in range(len(contours)):
            color_contours = (0, 0, 255)
            color = (255,0,0)
            cv2.drawContours(drawing, contours,i,color_contours,1,8)
            if len(contours) > 0:
                maxContour = max(contours,key= cv2.contourArea)
        # Drawing the convexhull
        if len(contours)>0:
            for i in range(2):
                hull.append(cv2.convexHull(maxContour))
                cv2.drawContours(drawing,hull,i,color,1,8)
                normArray = np.array(hull, dtype=object)

                centerHandY, centerHandX, smallX, bigX, smallY, bigY, smallXY, bigXY, smallYX, bigYX = features.calculateCenter(normArray[i])
                _, _, ratioLR = features.calcPixelsLeftRight(threshold, centerHandY)
                _, circularity = features.calculatePeriCirc(maxContour)
                yDist = bigY-smallY
                xDist = bigX-smallX
                thresholdResize = threshold[smallX:bigX, smallY:bigY]
                array = np.array(thresholdResize)
                whitePixel, blackpix, ratioBounding = features.boundingbox(array, yDist, xDist)
                amountFarPoints = features.convexity(maxContour)
                arrayTest = [1,1,1,1,1,1]
                arrayTest = [ratioLR,amountFarPoints,ratioBounding, circularity]
                newCompareInputTemplate(arrayTest)

        cv2.imshow("Convex",drawing)

    # press 'Q' if you want to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        _, bg = cap.read()

# When everything done, release the capture
cap.release()
# Destroy all the windows now
cv2.destroyAllWindow()
