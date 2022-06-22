import numpy as np
import cv2
import os
import features

# OS Paths to the different template image folders
root = os.path.abspath(os.getcwd())

path_to_data = os.path.join(root, "Template-image/pause")
imgsPause = os.listdir(path_to_data)

path_to_data = os.path.join(root, "Template-image/volumeup")
imgsVolumeup = os.listdir(path_to_data)

path_to_data = os.path.join(root, "Template-image/volumedown")
imgsVolumedown = os.listdir(path_to_data)

path_to_data = os.path.join(root, "Template-image/songnext")
imgsSongnext = os.listdir(path_to_data)

path_to_data = os.path.join(root, "Template-image/songprevious")
imgsSongprevious = os.listdir(path_to_data)

path_to_data = os.path.join(root, "Template-image/default")
imgsDefault = os.listdir(path_to_data)

# Print amount of data loaded
print("## DATA ASSETS ## \n Up: "+str(len(imgsVolumeup))+" Down: "+str(len(imgsVolumedown))+" Next: "+str(len(imgsSongnext))+" Previous: "+str(len(imgsSongprevious))+" Pause: "+str(len(imgsPause))+" Default: "+str(len(imgsDefault)))

# "5" is a placeholder number, but don't change it to 0-4 by default, as they are template values.
currentGesture = 5
templateHolder = [[],[],[],[],[],[]]
dirHoldForloop = [imgsPause,imgsVolumeup,imgsVolumedown,imgsSongnext,imgsSongprevious,imgsDefault]
strHoldForloop = ["pause","volumeup","volumedown","songnext","songprevious","default"]

for i in range (len(strHoldForloop)):
    for x in range(len(dirHoldForloop[i])):
        template = cv2.imread("Template-image/"+strHoldForloop[i]+"/"+str(x)+".png",0)
        templateHolder[i].append(template)


def calculateData(dataset, iteration):
    ratioLR, amountFarPoints, ratioBounding, circularity = 0,0,0,0
    hull = []

    cv2.imshow('image', templateHolder[dataset][iteration])
    threshold = templateHolder[dataset][iteration]

    print("Dataset:",dataset,"iteration",iteration)
    (im2, contours, hierachy) = cv2.findContours(templateHolder[dataset][iteration], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros((templateHolder[dataset][iteration].shape[0], templateHolder[dataset][iteration].shape[1], 3), np.uint8)

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

        centerHandY, centerHandX, smallX, bigX, smallY, bigY, smallXY, bigXY, smallYX, bigYX = features.calculateCenter(normArray[i])
        imageLcount, imageRcount, ratioLR = features.calcPixelsLeftRight(threshold, centerHandY)
        perimeter, circularity = features.calculatePeriCirc(maxContour)

        yDist = bigY - smallY
        xDist = bigX - smallX
        thresholdResize = threshold[smallX:bigX, smallY:bigY]
        array = np.array(thresholdResize)
        whitePixel, blackpixels, ratioBounding = features.boundingbox(array, yDist, xDist)

        cv2.line(drawing, pt1=(smallXY, smallX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)
        cv2.line(drawing, pt1=(bigXY, bigX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)
        cv2.line(drawing, pt1=(smallY, smallYX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)
        cv2.line(drawing, pt1=(bigY, bigYX), pt2=(centerHandY, centerHandX), color=(0, 255, 0), thickness=1)

        amountFarPoints = features.convexity(maxContour)

    cv2.imshow("Convex", drawing)
    return ratioLR, amountFarPoints,ratioBounding,circularity


def main():
    # Function reading and writing to text documents made with help from: https://www.geeksforgeeks.org/reading-writing-text-files-python/
    # For-loop with a length of all hand gestures
    for m in range (len(templateHolder)):
        if m == 0: fileData = open("Template-image\dataset_pause.txt","w")
        if m == 1: fileData = open("Template-image\dataset_volumeup.txt","w")
        if m == 2: fileData = open("Template-image\dataset_volumedown.txt","w")
        if m == 3: fileData = open("Template-image\dataset_songnext.txt","w")
        if m == 4: fileData = open("Template-image\dataset_songprevious.txt","w")
        if m == 5: fileData = open("Template-image\dataset_default.txt","w")

        # For-loop with a length of all the templates within each hand gesture
        for p in range (len(templateHolder[m])):
            # Loads all the feature methods and receives the data for each feature
            dataOutput = calculateData(m, p)
            for a in range (len(dataOutput)):
                try:
                    dataWrite = (str(round(dataOutput[a], 2))+" ")
                except TypeError:
                    dataWrite = dataOutput[a]

                fileData.write(dataWrite)
                if a == len(dataOutput)-1:
                    fileData.write("\n")
            # cv2.waitKey(0) # Used for manual analyzing each individual hand gesture from the template folder
        fileData.close()


main()
