import numpy as np
import cv2
import os
import math

# Paths to template images
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

# Print amount of data loaded
print("## DATA ASSETS ## \n Up: "+str(len(imgsVolumeup))+" Down: "+str(len(imgsVolumedown))+" Next: "+str(len(imgsSongnext))+" Previous: "+str(len(imgsSongprevious))+" Pause: "+str(len(imgsPause)))


# "5" is a placeholder number, but don't change it to 0-4 by default, as they are template values.
currentGesture = 5
templateHolder = [[],[],[],[],[]]

# Load all the templates into a 2D array of hand templates from the directory
for i in range(len(imgsPause)):
    template = cv2.imread("Template-image/pause/"+str(i)+".png", 0)
    templateHolder[0].append(template)

for i in range(len(imgsVolumeup)):
    template = cv2.imread("Template-image/volumeup/"+str(i)+".png", 0)
    templateHolder[1].append(template)

for i in range(len(imgsVolumedown)):
    template = cv2.imread("Template-image/volumedown/"+str(i)+".png", 0)
    templateHolder[2].append(template)

for i in range(len(imgsSongnext)):
    template = cv2.imread("Template-image/songnext/"+str(i)+".png", 0)
    templateHolder[3].append(template)

for i in range(len(imgsSongprevious)):
    template = cv2.imread("Template-image/songprevious/"+str(i)+".png", 0)
    templateHolder[4].append(template)

hit = np.array([[255,255,255],
               [255,255,255],
               [255,255,255]])

def erotion(threshold):
    newArray = np.zeros((threshold.shape[0], threshold.shape[1], 3), np.uint8)
    for y in range(threshold.shape[0]):
        for x in range(threshold.shape[1]):
            crop = threshold[y:y+3,x:x+3]
            croparray = np.array(crop)
            if np.all(hit == croparray):
                newArray[y][x] = 255
    return newArray


def dilation(threshold):
    newArray = np.zeros((threshold.shape[0], threshold.shape[1], 3), np.uint8)

    for y in range(threshold.shape[0]):
        for x in range(threshold.shape[1]):
            crop = threshold[y:y+3,x:x+3]
            croparray = np.array(crop)
            if np.any(hit == croparray) and x > 1 and y > 1 and x < threshold.shape[1]-1 and y<threshold.shape[0]-1:
                newArray[y][x] = 255
                newArray[y][x+1] = 255
                newArray[y+1][x+1] = 255
                newArray[y+1][x] = 255
                newArray[y-1][x] = 255
                newArray[y][x-1] = 255
                newArray[y-1][x-1] = 255
    return newArray

def main():
    # https://www.geeksforgeeks.org/reading-writing-text-files-python/

    for m in range (len(templateHolder)):
        for p in range (len(imgsPause)):
            print("DataSet", m, "DataPoint:", p)
            cv2.imshow("Template",templateHolder[m][p])
            getDia = dilation(templateHolder[m][p],80)
            cv2.imshow("DialatedTemp",getDia)
            getEro = erotion(getDia,80)
            cv2.imshow("EroTemp",getEro)
            cv2.waitKey(0)


main()
