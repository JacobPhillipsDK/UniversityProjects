import numpy as np
import cv2
import os

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

cap = cv2.VideoCapture(0)

# Frame count used to make operations based on the amount of frames
frameCount = 0
# Reading the video file until finished
_, bg = cap.read()
cv2.imshow("frame2", bg)
grayFrameHSV = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

while True:
    frameCount = frameCount + 1
    if frameCount % 10 == 0:
        ret, frame = cap.read()

        # if video finished or no Video Input
        if not ret:
            break


        # Convert the frames to gray scale
        feedHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the difference between the background and input stream
        diff = cv2.absdiff(grayFrameHSV, feedHSV)

        blur = cv2.blur(diff, (5, 5))  # blur the image
        threshold = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow("thresh", threshold)

        print("enter")
        for path in range(len(templateHolder)):
            for i in range(len(templateHolder[path])):
                # loads a new template called "img" from the template array
                img = templateHolder[path][i]
                width, height = img.shape[::-1]

                # Template matching part
                res = cv2.matchTemplate(threshold, img, cv2.TM_CCOEFF_NORMED)
                thresholdValue = 0.8
                loc = np.where(res >= thresholdValue)

                # Runs through all the templates to find a match

                for pt in zip(*loc[::-1]):
                    if path != currentGesture:
                        if path == 0:
                            #Follwing line used for debugging
                            print("DataType: " + str(path)+" DataPosition: "+str(i))
                            print("I see a hand: Pause/Play")
                        if path == 1:
                            print("DataType: " + str(path) + " DataPosition: " + str(i))
                            print("I see a hand: VolumeUp")
                        if path == 2:
                            print("DataType: " + str(path) + " DataPosition: " + str(i))
                            print("I see a hand: VolumeDown")
                        if path == 3:
                            print("DataType: " + str(path) + " DataPosition: " + str(i))
                            print("I see a hand: SongNext")
                        if path == 4:
                            print("DataType: " + str(path) + " DataPosition: " + str(i))
                            print("I see a hand: SongPrevious")
                        #Prevents the program from calling the same hand sign multiple times
                        currentGesture = path
        print("exit")

    # press 'Q' if you want to exit
    if cv2.waitKey(1) & 0xFF == ord('s'):
        _, bg = cap.read()
        grayFrameHSV = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

    # press 'W' if you want to exit
    if cv2.waitKey(1) & 0xFF == ord('w'):
        break

# When everything done, release the capture
cap.release()
# Destroy the all windows now
cv2.destroyAllWindow()
